"""Auth endpoints: register và login."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

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
        return await user_service.create_user(
            email=payload.email, password=payload.password
        )
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
    access_token = create_access_token(user_id=user.id)
    return Token(access_token=access_token)
