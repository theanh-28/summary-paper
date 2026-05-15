"""Object Storage — Supabase Storage integration.

Upload/download/delete files trên Supabase Storage thay vì lưu trực tiếp trên ổ cứng local.
Điều này giải quyết vấn đề ephemeral filesystem trên PaaS (Render, Railway, Fly.io).
"""
from __future__ import annotations

import logging
import uuid
from io import BytesIO

from app.core.config import settings

logger = logging.getLogger(__name__)


def _get_supabase_client():
    """Lazy init Supabase client để tránh lỗi nếu chưa cấu hình."""
    from supabase import create_client
    return create_client(settings.supabase_url, settings.supabase_key)


async def upload_file_to_storage(
    file_bytes: bytes,
    original_filename: str,
    user_id: int,
    content_type: str = "application/octet-stream",
) -> dict:
    """
    Upload file lên Supabase Storage.
    
    Returns:
        dict: {"file_url": "...", "storage_path": "...", "storage_provider": "supabase"}
    """
    # Generate unique path: papers/{user_id}/{uuid}_{filename}
    file_ext = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "bin"
    safe_name = f"{uuid.uuid4().hex}.{file_ext}"
    storage_path = f"user_{user_id}/{safe_name}"

    try:
        client = _get_supabase_client()
        bucket = settings.supabase_bucket

        # Upload file
        client.storage.from_(bucket).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": content_type},
        )

        # Tạo public URL
        public_url = client.storage.from_(bucket).get_public_url(storage_path)

        logger.info("File uploaded to Supabase: %s", storage_path)
        return {
            "file_url": public_url,
            "storage_path": storage_path,
            "storage_provider": "supabase",
        }
    except Exception as e:
        logger.error("Failed to upload file to Supabase: %s", str(e))
        raise


async def delete_file_from_storage(storage_path: str) -> bool:
    """Xóa file khỏi Supabase Storage."""
    try:
        client = _get_supabase_client()
        client.storage.from_(settings.supabase_bucket).remove([storage_path])
        logger.info("File deleted from Supabase: %s", storage_path)
        return True
    except Exception as e:
        logger.error("Failed to delete file from Supabase: %s", str(e))
        return False


async def download_file_from_storage(storage_path: str) -> bytes:
    """Download file từ Supabase Storage (cho worker dùng khi cần extract text)."""
    try:
        client = _get_supabase_client()
        data = client.storage.from_(settings.supabase_bucket).download(storage_path)
        return data
    except Exception as e:
        logger.error("Failed to download file from Supabase: %s", str(e))
        raise
