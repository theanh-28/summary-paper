"""Paper CRUD routes — tất cả đều yêu cầu xác thực JWT."""
from __future__ import annotations

import asyncio
import logging
import os
import uuid

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.paper_repository import PaperRepository
from app.repositories.user_repository import UserRepository
from app.schemas.paper import PaperCreate, PaperRead, PaperUpdate
from app.services.paper_service import PaperService
from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.docx_utils import extract_text_from_docx

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])

# Thư mục chứa file upload
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Giới hạn file upload: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {"application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}


@router.post("/upload", response_model=PaperRead, status_code=status.HTTP_201_CREATED)
async def upload_and_create_paper(
    title: str = Form(..., description="Tiêu đề của bài báo", max_length=500),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload một file PDF/TXT/DOCX lên server, tự động trích xuất nội dung và lưu vào database.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="File không hợp lệ")

    # Lấy đuôi file (ví dụ: '.pdf' hoặc '.txt')
    file_ext = os.path.splitext(file.filename)[1].lower()

    # --- Validate file extension ---
    if file_ext not in [".pdf", ".txt", ".docx"]:
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file định dạng PDF, TXT hoặc DOCX")

    # --- Validate MIME type ---
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="File không đúng định dạng PDF, TXT hoặc DOCX")

    # --- Generate safe filename (no path traversal) ---
    safe_filename = f"user_{current_user.id}_{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    # --- Cấu hình đọc theo Chunk (khối lượng nhỏ) ---
    CHUNK_SIZE = 1024 * 1024  # Đọc 1MB mỗi lần
    uploaded_size = 0

    try:
        # Mở file đích để ghi dần
        async with aiofiles.open(file_path, 'wb') as out_file:
            # Đọc từng chunk của file upload thay vì đọc tất cả vào RAM
            while chunk := await file.read(CHUNK_SIZE):
                uploaded_size += len(chunk)
                
                # Kiểm tra dung lượng LIÊN TỤC trong lúc đang tải
                if uploaded_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400, 
                        detail="File quá lớn. Giới hạn 10MB."
                    )
                # Ghi ngay chunk vừa đọc xuống đĩa cứng
                await out_file.write(chunk)

        # --- TRÍCH XUẤT TEXT TÙY THEO ĐỊNH DẠNG FILE ---
        if file_ext == ".pdf":
            # Chạy trong thread pool vì là blocking I/O
            extracted_text, page_count = await asyncio.to_thread(extract_text_from_pdf, file_path)
        elif file_ext == ".docx":
            extracted_text, page_count = await asyncio.to_thread(extract_text_from_docx, file_path)
        else:
            # Nếu là file .txt, đọc trực tiếp bằng utf-8
            async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                extracted_text = await f.read()
            page_count = 1  # File text mặc định gán là 1 trang

        # Lưu vào database
        paper_service = PaperService(PaperRepository(db), UserRepository(db))
        paper = await paper_service.create_paper(
            user_id=current_user.id,
            title=title,
            content=extracted_text,
            file_path=file_path,
            page_count=page_count,
        )
        logger.info("Paper uploaded: id=%s user=%s file=%s", paper.id, current_user.id, safe_filename)
        return paper

    except Exception as e:
        # Cleanup (Xóa) file ngay lập tức nếu có lỗi xảy ra
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
        
        # Nếu lỗi là do chúng ta ném ra (HTTPException 400)
        if isinstance(e, HTTPException):
            raise e
            
        # Các lỗi hệ thống khác
        logger.error("Error processing uploaded file for user %s: %s", current_user.id, str(e))
        raise HTTPException(status_code=500, detail="Lỗi khi xử lý file. Vui lòng thử lại.")


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
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
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