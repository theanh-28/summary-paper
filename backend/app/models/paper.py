"""Paper ORM model — lưu thông tin bài báo được upload.

Đã refactor:
- ENUM → VARCHAR(50) cho status (dễ mở rộng, tránh lock table khi ALTER)
- Thêm file_url, storage_path, storage_provider cho Object Storage
- Thêm index cho các cột thường query (status, created_at, user_id)
"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Index
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(LONGTEXT, nullable=True)
    
    # --- File Storage ---
    file_path = Column(String(1024), nullable=True)         # Legacy: local file path
    file_url = Column(String(2048), nullable=True)          # Object Storage public URL
    storage_path = Column(String(1024), nullable=True)      # Object Storage internal path (for delete)
    storage_provider = Column(String(50), nullable=True)    # "local" | "supabase"
    
    # --- Metadata ---
    page_count = Column(Integer, nullable=True)
    
    # --- State Machine ---
    # VARCHAR thay vì ENUM để tránh table lock khi ALTER và dễ mở rộng
    status = Column(
        String(50), nullable=False, default="uploaded", server_default="uploaded"
    )
    processing_time_seconds = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # --- Timestamps ---
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # --- Relationships ---
    user = relationship("User", backref="papers")
    summaries = relationship("Summary", back_populates="paper", cascade="all, delete-orphan")

    # --- Database Indexes ---
    __table_args__ = (
        Index("idx_papers_status", "status"),
        Index("idx_papers_created_at", "created_at"),
    )
