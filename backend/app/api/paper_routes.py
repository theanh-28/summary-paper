from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.paper_repository import PaperRepository
from app.repositories.user_repository import UserRepository
from app.schemas.paper import PaperCreate, PaperRead, PaperUpdate
from app.services.paper_service import PaperService

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])


@router.post("/", response_model=PaperRead, status_code=status.HTTP_201_CREATED)
async def create_paper(payload: PaperCreate, db: AsyncSession = Depends(get_db)):
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    try:
        return await paper_service.create_paper(
            user_id=payload.user_id,
            title=payload.title,
            content=payload.content,
            file_path=payload.file_path,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{paper_id}", response_model=PaperRead)
async def get_paper(paper_id: int, db: AsyncSession = Depends(get_db)):
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    paper = await paper_service.get_paper_by_id(paper_id)
    if not paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found")
    return paper


@router.get("/", response_model=list[PaperRead])
async def list_papers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    return await paper_service.list_papers(skip=skip, limit=limit)


@router.put("/{paper_id}", response_model=PaperRead)
async def update_paper(
    paper_id: int,
    payload: PaperUpdate,
    # TODO: Thay owner_id bằng current_user.id khi JWT đã được tích hợp
    owner_id: int,
    db: AsyncSession = Depends(get_db),
):
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    try:
        paper = await paper_service.update_paper(
            paper_id=paper_id,
            owner_id=owner_id,
            title=payload.title,
            content=payload.content,
            file_path=payload.file_path,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if not paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found or access denied")
    return paper


@router.delete("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paper(
    paper_id: int,
    # TODO: Thay owner_id bằng current_user.id khi JWT đã được tích hợp
    owner_id: int,
    db: AsyncSession = Depends(get_db),
):
    paper_service = PaperService(PaperRepository(db), UserRepository(db))
    deleted = await paper_service.delete_paper(paper_id=paper_id, owner_id=owner_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found or access denied")
