from __future__ import annotations
import logging
import os

from app.models.paper import Paper
from app.repositories.paper_repository import PaperRepository
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


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
        file_url: str | None = None,
        storage_path: str | None = None,
        storage_provider: str | None = None,
        page_count: int | None = None,
        status: str = "uploaded",
    ) -> Paper:
        # user_id đã được verify bởi JWT dependency ở route layer,
        # không cần query DB thêm lần nữa
        return await self.paper_repository.create(
            user_id=user_id,
            title=title,
            content=content,
            file_path=file_path,
            file_url=file_url,
            storage_path=storage_path,
            storage_provider=storage_provider,
            page_count=page_count,
            status=status,
        )

    async def get_paper_by_id(self, paper_id: int) -> Paper | None:
        return await self.paper_repository.get_by_id(paper_id)

    async def get_paper_by_owner(self, paper_id: int, owner_id: int) -> Paper | None:
        """Lấy paper chỉ khi thuộc về owner_id."""
        return await self.paper_repository.get_by_id_and_owner(
            paper_id=paper_id, user_id=owner_id
        )

    async def list_papers(self, skip: int = 0, limit: int = 100) -> list[Paper]:
        return await self.paper_repository.list(skip=skip, limit=limit)

    async def list_papers_by_owner(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Paper]:
        return await self.paper_repository.list_by_owner(
            user_id=user_id, skip=skip, limit=limit
        )

    async def update_paper(
        self,
        paper_id: int,
        owner_id: int,
        title: str | None = None,
        content: str | None = None,
        file_path: str | None = None,
        status: str | None = None,
        processing_time_seconds: int | None = None,
        error_message: str | None = None,
    ) -> Paper | None:
        # Kiểm tra tồn tại VÀ quyền sở hữu cùng lúc
        paper = await self.paper_repository.get_by_id_and_owner(
            paper_id=paper_id, user_id=owner_id
        )
        if not paper:
            return None
        return await self.paper_repository.update(
            paper=paper,
            title=title,
            content=content,
            file_path=file_path,
            status=status,
            processing_time_seconds=processing_time_seconds,
            error_message=error_message,
        )

    async def delete_paper(self, paper_id: int, owner_id: int) -> bool:
        # Chỉ xóa nếu paper thuộc về owner_id
        paper = await self.paper_repository.get_by_id_and_owner(
            paper_id=paper_id, user_id=owner_id
        )
        if not paper:
            return False
        
        file_path = paper.file_path
        storage_path = paper.storage_path
        storage_provider = paper.storage_provider
        
        await self.paper_repository.delete(paper)
        
        # Xóa file từ Object Storage nếu có
        if storage_provider == "supabase" and storage_path:
            try:
                from app.storage.supabase_storage import delete_file_from_storage
                await delete_file_from_storage(storage_path)
            except Exception as e:
                logger.error("Failed to delete file from storage: %s", str(e))
        
        # Xóa file local (backward compat)
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                logger.error("Failed to delete local file: %s", str(e))
                
        return True
