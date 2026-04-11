from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.info_service import InfoService
from src.api.services.news_service import NewsService
from src.db.database import get_session


async def get_news_service(session: AsyncSession = Depends(get_session)):
    return NewsService(session)


async def get_info_service(session: AsyncSession = Depends(get_session)):
    return InfoService(session)
