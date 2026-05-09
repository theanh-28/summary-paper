"""Auth endpoints: register và login."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.core.security import create_access_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Đăng ký tài khoản mới.
    - **email**: địa chỉ email hợp lệ, unique
    - **password**: tối thiểu 8 ký tự
    """
    user_service = UserService(UserRepository(db))
    try:
        user = await user_service.create_user(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name
        )
        logger.info("New user registered: id=%s email=%s full_name=%s", user.id, user.email, user.full_name)
        return user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Đăng nhập và nhận JWT access token.
    - Điền **email** vào trường `username`
    - Điền **password** vào trường `password`
    """
    user_service = UserService(UserRepository(db))
    user = await user_service.authenticate_user(
        email=form_data.username,   # OAuth2 dùng 'username', ta dùng email
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Kiểm tra tài khoản có active không
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact admin.",
        )

    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    access_token = create_access_token(user_id=user.id, role=user.role)
    logger.info("User logged in: id=%s role=%s", user.id, user.role)
    return Token(access_token=access_token, role=user.role)
