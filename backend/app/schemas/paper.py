from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PaperCreate(BaseModel):
    title: str


class PaperUpdate(BaseModel):
    title: str | None = None


class PaperRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    file_url: str | None = None
    storage_path: str | None = None
    status: str  # VARCHAR: uploaded, processing, completed, failed
    processing_time_seconds: int | None = None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime
