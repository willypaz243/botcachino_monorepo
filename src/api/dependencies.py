from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.content_service import ContentService
from src.db.database import get_session


async def get_content_service(session: AsyncSession = Depends(get_session)) -> ContentService:
    return ContentService(session)
