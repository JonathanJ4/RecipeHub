from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .config import settings


engine = create_async_engine(settings.database_url, pool_pre_ping=True)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for future SQLAlchemy models."""


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide one database session to a FastAPI request."""
    async with async_session_factory() as session:
        yield session


async def database_is_available() -> bool:
    """Verify that PostgreSQL accepts a simple query."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    return True


async def close_database() -> None:
    await engine.dispose()
