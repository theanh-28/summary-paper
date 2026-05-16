"""Async SQLAlchemy engine, session factory and Base declarative.

Connects to MySQL using the async aiomysql driver and exposes an
`AsyncSession` factory and the `get_db()` dependency generator.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Echo SQL during development for easier debugging.
# Pool pre-ping detects stale connections before use.
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,       # Số connection cố định trong pool
    max_overflow=20,    # Connection tạm thời khi vượt pool_size
    pool_recycle=3600,  # Recycle connections mỗi giờ để tránh timeout
    connect_args={
        "ssl": ssl_context,
        "init_command": "SET time_zone = '+07:00'",
        }
)

# Async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
