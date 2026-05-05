from app.models.summary import Summary
from app.repositories.paper_repository import PaperRepository
from app.repositories.summary_repository import SummaryRepository
from app.ml.summarizer import summarize


class SummaryService:
    def __init__(self, summary_repository: SummaryRepository, paper_repository: PaperRepository):
        self.summary_repository = summary_repository
        self.paper_repository = paper_repository

    async def create_summary(self, paper_id: int, owner_id: int, summary_type: str, content: str) -> Summary:
        paper = await self.paper_repository.get_by_id_and_owner(paper_id=paper_id, user_id=owner_id)
        if not paper:
            raise ValueError("Paper not found or access denied")
        return await self.summary_repository.create(
            paper_id=paper_id,
            summary_type=summary_type,
            content=content,
        )

    async def generate_and_save_summary(self, paper_id: int, owner_id: int, summary_type: str = "short") -> Summary:
        paper = await self.paper_repository.get_by_id_and_owner(paper_id=paper_id, user_id=owner_id)
        if not paper:
            raise ValueError("Paper not found or access denied")
            
        content_to_summarize = paper.content or ""
        
        # Gọi hàm async (gọi ra API bên ngoài)
        generated_text = await summarize(content_to_summarize)
        
        return await self.summary_repository.create(
            paper_id=paper_id,
            summary_type=summary_type,
            content=generated_text,
        )


    async def get_summary_by_id(self, summary_id: int, owner_id: int) -> Summary | None:
        summary = await self.summary_repository.get_by_id(summary_id)
        if not summary:
            return None
        paper = await self.paper_repository.get_by_id_and_owner(paper_id=summary.paper_id, user_id=owner_id)
        if not paper:
            return None
        return summary

    async def list_summaries_by_paper(self, paper_id: int, owner_id: int, skip: int = 0, limit: int = 100) -> list[Summary]:
        paper = await self.paper_repository.get_by_id_and_owner(paper_id=paper_id, user_id=owner_id)
        if not paper:
            raise ValueError("Paper not found or access denied")
        return await self.summary_repository.list_by_paper(paper_id=paper_id, skip=skip, limit=limit)

    async def update_summary(
        self,
        summary_id: int,
        owner_id: int,
        summary_type: str | None = None,
        content: str | None = None,
    ) -> Summary | None:
        summary = await self.summary_repository.get_by_id(summary_id)
        if not summary:
            return None
        paper = await self.paper_repository.get_by_id_and_owner(paper_id=summary.paper_id, user_id=owner_id)
        if not paper:
            return None
        return await self.summary_repository.update(
            summary=summary,
            summary_type=summary_type,
            content=content,
        )

    async def delete_summary(self, summary_id: int, owner_id: int) -> bool:
        summary = await self.summary_repository.get_by_id(summary_id)
        if not summary:
            return False
        paper = await self.paper_repository.get_by_id_and_owner(paper_id=summary.paper_id, user_id=owner_id)
        if not paper:
            return False
        await self.summary_repository.delete(summary)
        return True
