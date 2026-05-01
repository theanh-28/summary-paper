from app.models.summary import Summary
from app.repositories.paper_repository import PaperRepository
from app.repositories.summary_repository import SummaryRepository


class SummaryService:
    def __init__(self, summary_repository: SummaryRepository, paper_repository: PaperRepository):
        self.summary_repository = summary_repository
        self.paper_repository = paper_repository

    async def create_summary(self, paper_id: int, summary_type: str, content: str) -> Summary:
        paper = await self.paper_repository.get_by_id(paper_id)
        if not paper:
            raise ValueError("Paper not found")
        return await self.summary_repository.create(
            paper_id=paper_id,
            summary_type=summary_type,
            content=content,
        )

    async def get_summary_by_id(self, summary_id: int) -> Summary | None:
        return await self.summary_repository.get_by_id(summary_id)

    async def list_summaries(self, skip: int = 0, limit: int = 100) -> list[Summary]:
        return await self.summary_repository.list(skip=skip, limit=limit)

    async def list_summaries_by_paper(self, paper_id: int, skip: int = 0, limit: int = 100) -> list[Summary]:
        return await self.summary_repository.list_by_paper(paper_id=paper_id, skip=skip, limit=limit)

    async def update_summary(
        self,
        summary_id: int,
        summary_type: str | None = None,
        content: str | None = None,
    ) -> Summary | None:
        summary = await self.summary_repository.get_by_id(summary_id)
        if not summary:
            return None
        return await self.summary_repository.update(
            summary=summary,
            summary_type=summary_type,
            content=content,
        )

    async def delete_summary(self, summary_id: int) -> bool:
        summary = await self.summary_repository.get_by_id(summary_id)
        if not summary:
            return False
        await self.summary_repository.delete(summary)
        return True
