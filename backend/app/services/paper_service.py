from __future__ import annotations
import os

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
        # user_id đã được verify bởi JWT dependency ở route layer,
        # không cần query DB thêm lần nữa
        return await self.paper_repository.create(
            user_id=user_id,
            title=title,
            content=content,
            file_path=file_path,
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
        )

    async def delete_paper(self, paper_id: int, owner_id: int) -> bool:
        # Chỉ xóa nếu paper thuộc về owner_id
        paper = await self.paper_repository.get_by_id_and_owner(
            paper_id=paper_id, user_id=owner_id
        )
        if not paper:
            return False
        
        file_path = paper.file_path
        
        await self.paper_repository.delete(paper)
        
        # Xóa file vật lý nếu có
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # Log error if needed, but don't fail the deletion
                pass
                
        return True
