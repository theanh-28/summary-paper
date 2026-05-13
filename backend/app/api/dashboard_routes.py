"""Dashboard embedding routes — Metabase signed embedding."""
from __future__ import annotations

import logging
import time

import jwt as pyjwt

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.deps import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


def _generate_metabase_token(dashboard_id: int, params: dict | None = None) -> str:
    """
    Tạo Metabase signed JWT token.
    """
    payload = {
        "resource": {"dashboard": dashboard_id},
        "params": params or {},
        "exp": int(time.time()) + (60 * 10),  # Token hết hạn sau 10 phút
    }
    return pyjwt.encode(payload, settings.metabase_secret_key, algorithm="HS256")


def _generate_metabase_embed_url(token: str) -> str:
    """
    Tạo Metabase signed embedding URL từ token (dành cho iframe cũ).
    """
    return f"{settings.metabase_site_url}/embed/dashboard/{token}#bordered=true&titled=true"


@router.get("/embed-url")
async def get_embed_url(current_user: User = Depends(get_current_user)):
    """
    Trả về Metabase embed URL tùy theo role của user.

    - **Admin**: Dashboard tổng quan hệ thống, không filter.
    - **User**: Dashboard cá nhân, filter theo user_id.
    """
    if not settings.metabase_secret_key:
        return {
            "embed_url": None,
            "message": "Metabase chưa được cấu hình. Vui lòng set METABASE_SECRET_KEY.",
            "role": current_user.role,
        }

    if current_user.role in ["admin", "root"]:
        token = _generate_metabase_token(
            dashboard_id=settings.metabase_admin_dashboard_id,
            params={},  # Admin xem tất cả, không filter
        )
    else:
        token = _generate_metabase_token(
            dashboard_id=settings.metabase_user_dashboard_id,
            params={"id": current_user.id},  # Filter theo user_id
        )

    embed_url = _generate_metabase_embed_url(token)

    logger.info("Generated Metabase embed URL/Token for user %s (role=%s)", current_user.id, current_user.role)
    return {
        "embed_url": embed_url,
        "token": token,
        "role": current_user.role,
    }
