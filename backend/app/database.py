from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


engine = create_async_engine(settings.database_url, pool_pre_ping=True)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def database_is_available() -> bool:
    """Verify that PostgreSQL accepts a simple query."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    return True


async def close_database() -> None:
    await engine.dispose()
