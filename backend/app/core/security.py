"""JWT token creation and verification utilities."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(user_id: int, role: str = "user") -> str:
    """Tạo JWT access token chứa user_id và role trong claims.

    Claims:
        sub  — user_id as string
        role — "admin" | "user"
        exp  — expiration timestamp
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict | None:
    """Decode JWT và trả về payload dict, hoặc None nếu token không hợp lệ / hết hạn.

    Returns:
        dict with keys: user_id (int), role (str)  — or None on failure.
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            return None
        return {
            "user_id": int(user_id_str),
            "role": payload.get("role", "user"),
        }
    except (JWTError, ValueError):
        return None
