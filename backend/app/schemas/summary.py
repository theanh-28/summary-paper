from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class SummaryCreate(BaseModel):
    paper_id: int
    content: str


class SummaryGenerate(BaseModel):
    paper_id: int



class SummaryUpdate(BaseModel):
    content: str | None = None


class SummaryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paper_id: int
    content: str
    created_at: datetime

