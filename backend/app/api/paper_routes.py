"""Paper CRUD routes — tất cả đều yêu cầu xác thực JWT."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.paper_repository import PaperRepository
from app.repositories.user_repository import UserRepository
from app.schemas.paper import PaperCreate, PaperRead, PaperUpdate
from app.services.paper_service import PaperService

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])


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
