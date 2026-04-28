from app.models.paper import Paper
from app.repositories.paper_repository import PaperRepository
from app.repositories.user_repository import UserRepository


class PaperService:
    def __init__(self, paper_repository: PaperRepository, user_repository: UserRepository):
        self.paper_repository = paper_repository
        self.user_repository = user_repository

    async def create_paper(
        self,
        user_id: int,
        title: str,
        content: str | None = None,
        file_path: str | None = None,
    ) -> Paper:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return await self.paper_repository.create(
            user_id=user_id,
            title=title,
            content=content,
            file_path=file_path,
        )

    async def get_paper_by_id(self, paper_id: int) -> Paper | None:
        return await self.paper_repository.get_by_id(paper_id)

    async def list_papers(self) -> list[Paper]:
        return await self.paper_repository.list()

    async def update_paper(
        self,
        paper_id: int,
        user_id: int | None = None,
        title: str | None = None,
        content: str | None = None,
        file_path: str | None = None,
    ) -> Paper | None:
        paper = await self.paper_repository.get_by_id(paper_id)
        if not paper:
            return None
        if user_id is not None:
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
        return await self.paper_repository.update(
            paper=paper,
            user_id=user_id,
            title=title,
            content=content,
            file_path=file_path,
        )

    async def delete_paper(self, paper_id: int) -> bool:
        paper = await self.paper_repository.get_by_id(paper_id)
        if not paper:
            return False
        await self.paper_repository.delete(paper)
        return True

