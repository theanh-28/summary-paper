from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, email: str, password: str) -> User:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already exists")
        hashed_password = hash_password(password)
        return await self.user_repository.create(email=email, password=hashed_password)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email)

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.user_repository.list(skip=skip, limit=limit)

    async def update_user(
        self, user_id: int, email: str | None = None, password: str | None = None
    ) -> User | None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None

        if email and email != user.email:
            existing_user = await self.user_repository.get_by_email(email)
            if existing_user:
                raise ValueError("Email already exists")

        hashed_password = hash_password(password) if password is not None else None
        return await self.user_repository.update(user=user, email=email, password=hashed_password)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return False
        await self.user_repository.delete(user)
        return True

