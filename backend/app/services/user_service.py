from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, email: str, password: str) -> User:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already exists")
        return await self.user_repository.create(email=email, password=password)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email)

