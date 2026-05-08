"""FastAPI dependencies — reusable Depends() để inject current user và kiểm tra role."""
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

_INACTIVE_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Account is deactivated",
)

_ADMIN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Admin privileges required",
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency inject vào bất kỳ route nào cần xác thực.
    Trả về User object nếu token hợp lệ và tài khoản active, raise 401/403 nếu không.
    """
    token_data = decode_access_token(token)
    if token_data is None:
        raise _CREDENTIALS_EXCEPTION

    user = await UserRepository(db).get_by_id(token_data["user_id"])
    if user is None:
        raise _CREDENTIALS_EXCEPTION

    # Kiểm tra tài khoản còn active không
    if not user.is_active:
        raise _INACTIVE_EXCEPTION

    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency cho các route chỉ dành cho admin.
    Kế thừa get_current_user (đã verify JWT + active) rồi kiểm tra role.
    """
    if current_user.role != "admin":
        raise _ADMIN_EXCEPTION
    return current_user
