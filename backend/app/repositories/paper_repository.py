from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.paper import Paper


class PaperRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        user_id: int,
        title: str,
        content: str | None = None,
        file_path: str | None = None,
    ) -> Paper:
        paper = Paper(user_id=user_id, title=title, content=content, file_path=file_path)
        self.db.add(paper)
        await self.db.commit()
        await self.db.refresh(paper)
        return paper

    async def get_by_id(self, paper_id: int) -> Paper | None:
        result = await self.db.execute(select(Paper).where(Paper.id == paper_id))
        return result.scalar_one_or_none()

    async def list(self) -> list[Paper]:
        result = await self.db.execute(select(Paper).order_by(Paper.id))
        return list(result.scalars().all())

    async def update(
        self,
        paper: Paper,
        user_id: int | None = None,
        title: str | None = None,
        content: str | None = None,
        file_path: str | None = None,
    ) -> Paper:
        if user_id is not None:
            paper.user_id = user_id
        if title is not None:
            paper.title = title
        if content is not None:
            paper.content = content
        if file_path is not None:
            paper.file_path = file_path
        await self.db.commit()
        await self.db.refresh(paper)
        return paper

    async def delete(self, paper: Paper) -> None:
        await self.db.delete(paper)
        await self.db.commit()

