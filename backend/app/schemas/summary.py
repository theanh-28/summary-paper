from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class SummaryCreate(BaseModel):
    paper_id: int
    type: Literal["short", "detailed"]
    content: str


class SummaryGenerate(BaseModel):
    paper_id: int
    type: Literal["short", "detailed"] = "short"



class SummaryUpdate(BaseModel):
    type: Literal["short", "detailed"] | None = None
    content: str | None = None


class SummaryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paper_id: int
    type: Literal["short", "detailed"]
    content: str
    created_at: datetime

