from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PaperCreate(BaseModel):
    title: str
    content: str | None = None
    file_path: str | None = None


class PaperUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    file_path: str | None = None


class PaperRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    content: str | None
    file_path: str | None
    created_at: datetime

