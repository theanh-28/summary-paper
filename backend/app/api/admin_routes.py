"""Admin-only routes — quản lý user, xem thống kê hệ thống."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_admin_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.paper_repository import PaperRepository
from app.repositories.summary_repository import SummaryRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead, UserRoleUpdate
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/stats")
async def get_system_stats(
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Thống kê tổng quan hệ thống — chỉ admin mới xem được.
    Trả về: tổng user, tổng papers, tổng summaries.
    """
    user_repo = UserRepository(db)
    paper_repo = PaperRepository(db)
    summary_repo = SummaryRepository(db)

    total_users = await user_repo.count()
    total_papers = await paper_repo.count()
    total_summaries = await summary_repo.count()

    return {
        "total_users": total_users,
        "total_papers": total_papers,
        "total_summaries": total_summaries,
    }


@router.get("/users", response_model=list[UserRead])
async def list_all_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Liệt kê tất cả user trong hệ thống (paginated). Chỉ admin."""
    user_service = UserService(UserRepository(db))
    return await user_service.list_users(skip=skip, limit=limit)


@router.put("/users/{user_id}/role", response_model=UserRead)
async def update_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Thay đổi role của user. Có kiểm tra cấp bậc."""
    if admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role",
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Kiểm tra phân quyền: admin thường không được sửa role của admin khác hoặc root
    if admin.role == "admin" and user.role in ("admin", "root"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this user's role",
        )

    # Admin thường cũng không được cấp quyền root cho người khác
    if admin.role == "admin" and payload.role == "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ROOT can assign root privileges",
        )

    user = await user_repo.update_role(user, payload.role)
    logger.info("Admin %s changed role of user %s to %s", admin.id, user_id, payload.role)
    return user


@router.put("/users/{user_id}/toggle-active", response_model=UserRead)
async def toggle_user_active(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Kích hoạt / vô hiệu hóa tài khoản user. Có kiểm tra cấp bậc."""
    if admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account",
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Kiểm tra phân quyền: admin thường không được khóa admin khác hoặc root
    if admin.role == "admin" and user.role in ("admin", "root"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to toggle this user's active status",
        )

    user = await user_repo.toggle_active(user)
    logger.info("Admin %s toggled active status of user %s to %s", admin.id, user_id, user.is_active)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_user(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Admin xóa user khỏi hệ thống. Có kiểm tra cấp bậc."""
    if admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account from admin panel",
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Kiểm tra phân quyền: admin thường không được xóa admin khác hoặc root
    if admin.role == "admin" and user.role in ("admin", "root"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user",
        )

    user_service = UserService(UserRepository(db))
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    logger.info("Admin %s deleted user %s", admin.id, user_id)
