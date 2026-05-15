"""User ORM model with RBAC support.

Đã refactor: ENUM → VARCHAR(50) cho role để tránh table lock khi ALTER.
Validation thực hiện ở tầng application (deps.py, service layer).
"""
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    # VARCHAR thay vì ENUM để tránh table lock khi ALTER và dễ mở rộng
    role = Column(
        String(50),
        nullable=False,
        default="user",
        server_default="user",
    )
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
