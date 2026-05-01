"""FastAPI dependencies — reusable Depends() để inject current user."""
from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

# tokenUrl trỏ tới endpoint login — Swagger UI sẽ dùng đây để hiển thị nút "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency inject vào bất kỳ route nào cần xác thực.
    Trả về User object nếu token hợp lệ, raise 401 nếu không.
    """
    user_id = decode_access_token(token)
    if user_id is None:
        raise _CREDENTIALS_EXCEPTION

    user = await UserRepository(db).get_by_id(user_id)
    if user is None:
        raise _CREDENTIALS_EXCEPTION

    return user
