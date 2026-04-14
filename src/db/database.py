from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

async_engine = create_async_engine(settings.database.url.get_secret_value(), echo=True)

async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables():
    from sqlmodel import SQLModel

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
