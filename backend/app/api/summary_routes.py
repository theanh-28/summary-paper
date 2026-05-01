"""Summary CRUD routes — POST/PUT/DELETE yêu cầu JWT."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.paper_repository import PaperRepository
from app.repositories.summary_repository import SummaryRepository
from app.schemas.summary import SummaryCreate, SummaryRead, SummaryUpdate
from app.services.summary_service import SummaryService

router = APIRouter(prefix="/api/v1/summaries", tags=["summaries"])


@router.post("/", response_model=SummaryRead, status_code=status.HTTP_201_CREATED)
async def create_summary(
    payload: SummaryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Tạo bản tóm tắt cho một paper."""
    summary_service = SummaryService(SummaryRepository(db), PaperRepository(db))
    try:
        return await summary_service.create_summary(
            paper_id=payload.paper_id,
            summary_type=payload.type,
            content=payload.content,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


# ⚠️ Route cụ thể phải đặt TRƯỚC route có path param /{summary_id}
@router.get("/", response_model=list[SummaryRead])
async def list_summaries(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy toàn bộ summaries (có phân trang)."""
    summary_service = SummaryService(SummaryRepository(db), PaperRepository(db))
    return await summary_service.list_summaries(skip=skip, limit=limit)


@router.get("/by-paper/{paper_id}", response_model=list[SummaryRead])
async def list_summaries_by_paper(
    paper_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy tất cả summaries của một paper cụ thể."""
    summary_service = SummaryService(SummaryRepository(db), PaperRepository(db))
    return await summary_service.list_summaries_by_paper(
        paper_id=paper_id, skip=skip, limit=limit
    )


@router.get("/{summary_id}", response_model=SummaryRead)
async def get_summary(
    summary_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy chi tiết 1 summary."""
    summary_service = SummaryService(SummaryRepository(db), PaperRepository(db))
    summary = await summary_service.get_summary_by_id(summary_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )
    return summary


@router.put("/{summary_id}", response_model=SummaryRead)
async def update_summary(
    summary_id: int,
    payload: SummaryUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cập nhật nội dung summary."""
    summary_service = SummaryService(SummaryRepository(db), PaperRepository(db))
    summary = await summary_service.update_summary(
        summary_id=summary_id,
        summary_type=payload.type,
        content=payload.content,
    )
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )
    return summary


@router.delete("/{summary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_summary(
    summary_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Xóa summary."""
    summary_service = SummaryService(SummaryRepository(db), PaperRepository(db))
    deleted = await summary_service.delete_summary(summary_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )
