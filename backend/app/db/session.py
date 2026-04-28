"""Async SQLAlchemy engine, session factory and Base declarative.

Connects to MySQL using the async aiomysql driver and exposes an
`AsyncSession` factory and the `get_db()` dependency generator.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Echo SQL during development for easier debugging
engine = create_async_engine(settings.database_url, echo=settings.debug, pool_pre_ping=True)

# Async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
