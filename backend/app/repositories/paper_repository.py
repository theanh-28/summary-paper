from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.paper import Paper


class PaperRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        user_id: int,
        title: str,
        file_url: str | None = None,
        storage_path: str | None = None,
        status: str = "uploaded",
    ) -> Paper:
        paper = Paper(
            user_id=user_id, title=title,
            file_url=file_url, storage_path=storage_path,
            status=status,
        )
        self.db.add(paper)
        await self.db.commit()
        await self.db.refresh(paper)
        return paper

    async def get_by_id(self, paper_id: int) -> Paper | None:
        result = await self.db.execute(select(Paper).where(Paper.id == paper_id))
        return result.scalar_one_or_none()

    async def get_by_id_and_owner(self, paper_id: int, user_id: int) -> Paper | None:
        result = await self.db.execute(
            select(Paper).where(Paper.id == paper_id, Paper.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[Paper]:
        result = await self.db.execute(
            select(Paper).order_by(Paper.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def list_by_owner(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Paper]:
        result = await self.db.execute(
            select(Paper)
            .where(Paper.user_id == user_id)
            .order_by(Paper.created_at.desc())
            .offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.db.execute(select(func.count(Paper.id)))
        return result.scalar_one()

    async def update(
        self,
        paper: Paper,
        title: str | None = None,
        file_url: str | None = None,
        storage_path: str | None = None,
        status: str | None = None,
        processing_time_seconds: int | None = None,
        error_message: str | None = None,
    ) -> Paper:
        if title is not None:
            paper.title = title
        if file_url is not None:
            paper.file_url = file_url
        if storage_path is not None:
            paper.storage_path = storage_path
        if status is not None:
            paper.status = status
        if processing_time_seconds is not None:
            paper.processing_time_seconds = processing_time_seconds
        if error_message is not None:
            paper.error_message = error_message
        await self.db.commit()
        await self.db.refresh(paper)
        return paper

    async def delete(self, paper: Paper) -> None:
        await self.db.delete(paper)
        await self.db.commit()
