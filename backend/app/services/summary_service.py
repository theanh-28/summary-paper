from app.models.summary import Summary
from app.repositories.paper_repository import PaperRepository
from app.repositories.summary_repository import SummaryRepository
from app.ml.summarizer import summarize


class SummaryService:
    def __init__(self, summary_repository: SummaryRepository, paper_repository: PaperRepository):
        self.summary_repository = summary_repository
        self.paper_repository = paper_repository

    async def create_summary(self, paper_id: int, owner_id: int, content: str) -> Summary:
        paper = await self.paper_repository.get_by_id_and_owner(paper_id=paper_id, user_id=owner_id)
        if not paper:
            raise ValueError("Paper not found or access denied")
        return await self.summary_repository.create(
            paper_id=paper_id,
            content=content,
        )

    async def generate_and_save_summary(self, paper_id: int, owner_id: int) -> Summary:
        from datetime import datetime, timezone
        
        paper = await self.paper_repository.get_by_id_and_owner(paper_id=paper_id, user_id=owner_id)
        if not paper:
            raise ValueError("Paper not found or access denied")
            
        content_to_summarize = paper.content or ""
        
        start_time = datetime.now(timezone.utc)
        
        # Cập nhật trạng thái đang xử lý
        await self.paper_repository.update(paper=paper, status="processing")
        
        try:
            # Gọi hàm async (gọi ra API bên ngoài)
            generated_text = await summarize(content_to_summarize)
            
            end_time = datetime.now(timezone.utc)
            processing_time = int((end_time - start_time).total_seconds())
            
            await self.paper_repository.update(
                paper=paper,
                status="completed",
                processing_time_seconds=processing_time,
                error_message=""
            )
            
            return await self.summary_repository.create(
                paper_id=paper_id,
                content=generated_text,
            )
        except Exception as e:
            await self.paper_repository.update(
                paper=paper,
                status="failed",
                error_message=str(e)
            )
            raise ValueError(f"Failed to generate summary: {str(e)}")


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
