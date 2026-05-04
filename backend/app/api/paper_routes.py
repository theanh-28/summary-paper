"""Paper CRUD routes — tất cả đều yêu cầu xác thực JWT."""
from __future__ import annotations

import os
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.paper_repository import PaperRepository
from app.repositories.user_repository import UserRepository
from app.schemas.paper import PaperCreate, PaperRead, PaperUpdate
from app.services.paper_service import PaperService
from app.utils.pdf_utils import extract_text_from_pdf

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])

# Thư mục chứa file upload
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/upload", response_model=PaperRead, status_code=status.HTTP_201_CREATED)
async def upload_and_create_paper(
    title: str = Form(..., description="Tiêu đề của bài báo"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload một file PDF lên server, tự động trích xuất nội dung và lưu vào database.
    - File sẽ được lưu vào thư mục `uploads/`
    - Nội dung text sẽ được trích xuất bằng thư viện pypdf
    - Bài báo (Paper) mới sẽ được tự động tạo với nội dung vừa trích xuất
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file định dạng PDF")
        
    # Đảm bảo thư mục tồn tại (phòng hờ)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Tạo tên file độc nhất để tránh trùng lặp (có thể thêm timestamp hoặc user_id)
    safe_filename = f"user_{current_user.id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    try:
        # Đọc và ghi file theo dạng bất đồng bộ
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        # Trích xuất text từ file PDF vừa lưu
        extracted_text = extract_text_from_pdf(file_path)
        
        # Lưu vào database
        paper_service = PaperService(PaperRepository(db), UserRepository(db))
        paper = await paper_service.create_paper(
            user_id=current_user.id,
            title=title,
            content=extracted_text,
            file_path=file_path,
        )
        return paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý file: {str(e)}")

@router.post("/", response_model=PaperRead, status_code=status.HTTP_201_CREATED)
async def create_paper(
    payload: PaperCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Tạo bài báo mới. user_id lấy từ JWT token."""
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    return await paper_service.create_paper(
        user_id=current_user.id,
        title=payload.title,
        content=payload.content,
        file_path=payload.file_path,
    )


@router.get("/", response_model=list[PaperRead])
async def list_papers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy danh sách bài báo của user đang đăng nhập."""
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    return await paper_service.list_papers_by_owner(
        user_id=current_user.id, skip=skip, limit=limit
    )


@router.get("/{paper_id}", response_model=PaperRead)
async def get_paper(
    paper_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy chi tiết 1 bài báo. Chỉ trả về nếu thuộc về user đang đăng nhập."""
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    paper = await paper_service.get_paper_by_owner(
        paper_id=paper_id, owner_id=current_user.id
    )
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found"
        )
    return paper


@router.put("/{paper_id}", response_model=PaperRead)
async def update_paper(
    paper_id: int,
    payload: PaperUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cập nhật bài báo. Chỉ chủ sở hữu mới được phép."""
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    paper = await paper_service.update_paper(
        paper_id=paper_id,
        owner_id=current_user.id,
        title=payload.title,
        content=payload.content,
        file_path=payload.file_path,
    )
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found or access denied",
        )
    return paper


@router.delete("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paper(
    paper_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Xóa bài báo. Chỉ chủ sở hữu mới được phép."""
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    deleted = await paper_service.delete_paper(
        paper_id=paper_id, owner_id=current_user.id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found or access denied",
        )
