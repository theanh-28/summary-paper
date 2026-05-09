from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    file_path = Column(String(1024), nullable=True)
    page_count = Column(Integer, nullable=True)
    status = Column(Enum("uploaded", "processing", "completed", "failed", name="paper_status"), nullable=False, default="uploaded", server_default="uploaded")
    processing_time_seconds = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", backref="papers")
    summaries = relationship("Summary", back_populates="paper", cascade="all, delete-orphan")

