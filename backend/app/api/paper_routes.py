"""Paper CRUD routes — tất cả đều yêu cầu xác thực JWT.

Đã refactor:
- Upload trả response ngay (202 Accepted) trong < 1 giây
- Text extraction + AI summarization chạy trong background worker
- File lưu trữ hoàn toàn trên Supabase Object Storage
"""
from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.paper_repository import PaperRepository
from app.repositories.user_repository import UserRepository
from app.schemas.paper import PaperCreate, PaperRead, PaperUpdate
from app.services.paper_service import PaperService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])

# Giới hạn file upload: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# Các status hợp lệ cho state machine
VALID_STATUSES = {"uploaded", "processing", "completed", "failed"}


async def _enqueue_paper_task(paper_id: int) -> None:
    """Đẩy task xử lý paper vào Redis Queue (ARQ)."""
    try:
        from arq import create_pool
        from app.worker.worker_settings import WorkerSettings

        redis = await create_pool(WorkerSettings.redis_settings)
        await redis.enqueue_job(
            "process_paper_task",
            paper_id,
            _queue_name=WorkerSettings.queue_name,
        )
        logger.info("Enqueued paper processing task: paper_id=%s", paper_id)
    except Exception as e:
        logger.error("Failed to enqueue task for paper %s: %s", paper_id, str(e))
        raise


@router.post("/upload", response_model=PaperRead, status_code=status.HTTP_202_ACCEPTED)
async def upload_and_create_paper(
    title: str = Form(..., description="Tiêu đề của bài báo", max_length=500),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload file PDF/TXT/DOCX lên Supabase Storage.
    
    **Kiến trúc (Async)**:
    1. Nhận file
    2. Upload lên Supabase Object Storage
    3. Tạo record trong database (status=uploaded)
    4. Đẩy task vào Redis Queue cho worker xử lý
    5. Trả response ngay lập tức (202 Accepted) — KHÔNG chờ AI
    
    Frontend sẽ polling GET /papers/{id} để theo dõi trạng thái.
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

    # --- Đọc toàn bộ file vào buffer (giới hạn 10MB) ---
    CHUNK_SIZE = 1024 * 1024  # 1MB
    file_bytes = bytearray()
    while chunk := await file.read(CHUNK_SIZE):
        file_bytes.extend(chunk)
        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File quá lớn. Giới hạn 10MB.")

    file_bytes = bytes(file_bytes)

    # --- Upload lên Supabase Storage ---
    if not settings.supabase_url or not settings.supabase_key:
        raise HTTPException(
            status_code=500,
            detail="Supabase chưa được cấu hình. Vui lòng liên hệ quản trị viên."
        )

    try:
        from app.storage.supabase_storage import upload_file_to_storage
        result = await upload_file_to_storage(
            file_bytes=file_bytes,
            original_filename=file.filename,
            user_id=current_user.id,
            content_type=file.content_type or "application/octet-stream",
        )
        file_url = result["file_url"]
        storage_path_val = result["storage_path"]
    except Exception as e:
        logger.error("Supabase upload failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Lỗi khi upload file lên storage. Vui lòng thử lại.")

    try:
        # --- Tạo DB record (status=uploaded, CHƯA extract text) ---
        paper_service = PaperService(PaperRepository(db), UserRepository(db))
        paper = await paper_service.create_paper(
            user_id=current_user.id,
            title=title,
            file_url=file_url,
            storage_path=storage_path_val,
            status="uploaded",
        )

        # --- Đẩy task vào background worker ---
        try:
            await _enqueue_paper_task(paper.id)
        except Exception as e:
            logger.warning(
                "Failed to enqueue worker task for paper %s: %s. "
                "Paper saved but won't be processed until worker is available.",
                paper.id, str(e)
            )

        logger.info(
            "Paper uploaded: id=%s user=%s storage=supabase",
            paper.id, current_user.id
        )
        return paper

    except HTTPException:
        raise
    except Exception as e:
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
    )


@router.get("/", response_model=list[PaperRead])
async def list_papers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy danh sách bài báo của user đang đăng nhập (mới nhất trước)."""
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
    """
    Lấy chi tiết 1 bài báo. Chỉ trả về nếu thuộc về user đang đăng nhập.
    
    Frontend sử dụng endpoint này để polling trạng thái:
    - status=uploaded → đang chờ xử lý
    - status=processing → worker đang extract + summarize
    - status=completed → hoàn tất, có thể xem summary
    - status=failed → lỗi, xem error_message
    """
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