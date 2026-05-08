from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, email: str, password: str, role: str = "user") -> User:
        user = User(email=email, password=password, role=role)
        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            raise ValueError("Email already exists") from exc
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(select(User).order_by(User.id).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def count(self) -> int:
        """Đếm tổng số user."""
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar_one()

    async def update(self, user: User, email: str | None = None, password: str | None = None) -> User:
        if email is not None:
            user.email = email
        if password is not None:
            user.password = password
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            raise ValueError("Email already exists") from exc
        await self.db.refresh(user)
        return user

    async def update_role(self, user: User, role: str) -> User:
        """Cập nhật role của user. Dùng cho admin management."""
        user.role = role
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def toggle_active(self, user: User) -> User:
        """Đảo trạng thái active/inactive. Dùng cho admin management."""
        user.is_active = not user.is_active
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()
