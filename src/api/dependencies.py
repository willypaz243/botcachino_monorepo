from fastapi import Depends
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.content_service import ContentService
from src.api.services.embedding_service import EmbbedingService
from src.api.services.history_service import HistoryService
from src.db.database import get_session


async def get_emb_service():
    emb_model = HuggingFaceEmbeddings(
        model_name="jinaai/jina-embeddings-v2-base-es",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
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
