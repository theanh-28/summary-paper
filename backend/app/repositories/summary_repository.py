from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.summary import Summary


class SummaryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, paper_id: int, summary_type: str, content: str) -> Summary:
        summary = Summary(paper_id=paper_id, type=summary_type, content=content)
        self.db.add(summary)
        await self.db.commit()
        await self.db.refresh(summary)
        return summary

    async def get_by_id(self, summary_id: int) -> Summary | None:
        result = await self.db.execute(select(Summary).where(Summary.id == summary_id))
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[Summary]:
        result = await self.db.execute(select(Summary).order_by(Summary.id).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def list_by_paper(self, paper_id: int, skip: int = 0, limit: int = 100) -> list[Summary]:
        """Chỉ trả về các summary thuộc về paper_id."""
        result = await self.db.execute(
            select(Summary)
            .where(Summary.paper_id == paper_id)
            .order_by(Summary.id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(
        self,
        summary: Summary,
        summary_type: str | None = None,
        content: str | None = None,
    ) -> Summary:
        if summary_type is not None:
            summary.type = summary_type
        if content is not None:
            summary.content = content
        await self.db.commit()
        await self.db.refresh(summary)
        return summary

    async def delete(self, summary: Summary) -> None:
        await self.db.delete(summary)
        await self.db.commit()
