"""Summary CRUD routes — POST/PUT/DELETE yêu cầu JWT.

Đã refactor:
- /generate endpoint giờ cũng sử dụng background worker (nếu paper đã có content)
- Giữ backward compat cho trường hợp gọi trực tiếp
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.paper_repository import PaperRepository
from app.repositories.summary_repository import SummaryRepository
from app.schemas.summary import SummaryCreate, SummaryGenerate, SummaryRead, SummaryUpdate
from app.services.summary_service import SummaryService

logger = logging.getLogger(__name__)

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
            owner_id=current_user.id,
            content=payload.content,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/generate", status_code=status.HTTP_202_ACCEPTED)
async def generate_summary(
    payload: SummaryGenerate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Tự động tạo bản tóm tắt cho một paper bằng AI.
    
    **Kiến trúc mới**: Đẩy task vào background worker, trả 202 Accepted ngay.
    Frontend polling GET /papers/{id} để theo dõi trạng thái.
    """
    paper_repo = PaperRepository(db)
    paper = await paper_repo.get_by_id_and_owner(
        paper_id=payload.paper_id, user_id=current_user.id
    )
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found or access denied"
        )

    # Nếu paper đã completed, cho phép re-generate
    if paper.status in ("processing",):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Paper đang được xử lý. Vui lòng chờ."
        )

    # Enqueue background task
    try:
        from arq import create_pool
        from app.worker.worker_settings import WorkerSettings

        # Reset status
        paper.status = "uploaded"
        paper.error_message = ""
        await db.commit()

        redis = await create_pool(WorkerSettings.redis_settings)
        await redis.enqueue_job(
            "process_paper_task",
            paper.id,
            _queue_name=WorkerSettings.queue_name,
        )
        logger.info("Re-enqueued paper processing task: paper_id=%s", paper.id)
    except Exception as e:
        logger.error("Failed to enqueue task: %s", str(e))
        # Fallback: xử lý trực tiếp (synchronous) nếu worker không khả dụng
        logger.warning("Falling back to synchronous processing for paper %s", paper.id)
        summary_service = SummaryService(SummaryRepository(db), paper_repo)
        try:
            result = await summary_service.generate_and_save_summary(
                paper_id=payload.paper_id,
                owner_id=current_user.id,
            )
            return result
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
            ) from exc

    return {
        "message": "Đã đưa vào hàng đợi xử lý. Theo dõi trạng thái tại GET /papers/{id}",
        "paper_id": paper.id,
        "status": "uploaded",
    }


@router.get("/by-paper/{paper_id}", response_model=list[SummaryRead])
async def list_summaries_by_paper(
    paper_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy tất cả summaries của một paper cụ thể."""
    summary_service = SummaryService(SummaryRepository(db), PaperRepository(db))
    try:
        return await summary_service.list_summaries_by_paper(
            paper_id=paper_id, owner_id=current_user.id, skip=skip, limit=limit
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found or access denied"
        ) from exc


@router.get("/{summary_id}", response_model=SummaryRead)
async def get_summary(
    summary_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy chi tiết 1 summary."""
    summary_service = SummaryService(SummaryRepository(db), PaperRepository(db))
    summary = await summary_service.get_summary_by_id(summary_id, current_user.id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found or access denied"
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
        owner_id=current_user.id,
        content=payload.content,
    )
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found or access denied"
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
    deleted = await summary_service.delete_summary(summary_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found or access denied"
        )
