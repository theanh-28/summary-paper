"""Paper ORM model — lưu thông tin bài báo được upload.

Đã refactor:
- ENUM → VARCHAR(50) cho status (dễ mở rộng, tránh lock table khi ALTER)
- File lưu trữ hoàn toàn trên Supabase (file_url, storage_path)
- Không lưu content vào DB (worker giữ trong RAM, gửi AI xong bỏ)
- Thêm index cho các cột thường query (status, created_at, user_id)
"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String(500), nullable=False)
    
    # --- File Storage (Supabase only) ---
    file_url = Column(String(2048), nullable=True)          # Supabase public URL
    storage_path = Column(String(1024), nullable=True)      # Supabase internal path (for download/delete)
    
    # --- State Machine ---
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
