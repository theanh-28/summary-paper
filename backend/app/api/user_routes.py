"""User routes — profile management cho user đang đăng nhập."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead, UserUpdate, ChangePassword
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    """Lấy thông tin profile của user đang đăng nhập."""
    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy thông tin user. User thường chỉ xem được chính mình, admin xem được mọi user."""
    # Admin và Root có thể xem bất kỳ user nào
    if current_user.role not in ("admin", "root") and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user_service = UserService(UserRepository(db))
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cập nhật thông tin user. Chỉ chính user hoặc admin mới có quyền."""
    if current_user.role not in ("admin", "root") and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user_service = UserService(UserRepository(db))
    target_user = await user_service.get_user_by_id(user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Admin thường không được update thông tin của admin khác hoặc root
    if current_user.id != user_id and current_user.role == "admin" and target_user.role in ("admin", "root"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this user",
        )
    try:
        user = await user_service.update_user(
            user_id=user_id,
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/me/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    payload: ChangePassword,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Thay đổi mật khẩu cho user đang đăng nhập."""
    if payload.new_password != payload.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mật khẩu xác nhận không khớp")
    
    user_service = UserService(UserRepository(db))
    try:
        success = await user_service.change_password(
            user_id=current_user.id,
            current_password=payload.current_password,
            new_password=payload.new_password
        )
        if not success:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"detail": "Đổi mật khẩu thành công"}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xóa user. Chỉ chính user hoặc admin mới có quyền."""
    if current_user.role not in ("admin", "root") and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user_service = UserService(UserRepository(db))
    target_user = await user_service.get_user_by_id(user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Admin thường không được xóa admin khác hoặc root
    if current_user.id != user_id and current_user.role == "admin" and target_user.role in ("admin", "root"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user",
        )
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
