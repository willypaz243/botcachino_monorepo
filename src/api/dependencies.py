from fastapi import Depends
from langchain_nebius import NebiusEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.content_service import ContentService
from src.api.services.embedding_service import EmbbedingService
from src.api.services.history_service import HistoryService
from src.config import settings
from src.db.database import get_session


async def get_emb_service():
    emb_model = NebiusEmbeddings(
        model=settings.nebius.emb_model,
        api_key=settings.nebius.api_key,
    )
    return EmbbedingService(emb_model)


async def get_content_service(
    session: AsyncSession = Depends(get_session),
    emb_service: EmbbedingService = Depends(get_emb_service),
) -> ContentService:
    return ContentService(session, emb_service)


async def get_history_service(
    session: AsyncSession = Depends(get_session),
) -> HistoryService:
    return HistoryService(session)
