from __future__ import annotations

from functools import cache
from typing import Any

from pydantic import SecretStr
from langchain_nebius import NebiusEmbeddings
from langchain_core.runnables import RunnableConfig
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.agent.graph import build_agent_graph
from src.agent.services import AgentServices
from src.api.services.content_service import ContentService
from src.api.services.embedding_service import EmbbedingService
from src.config import settings


@cache
def create_content_service() -> ContentService:
    engine = create_async_engine(
        settings.database.url.get_secret_value(),
        echo=False,
    )
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session: AsyncSession = async_session()

    api_key_value: SecretStr | None = None
    if settings.nebius.api_key:
        api_key_value = settings.nebius.api_key

    emb_model = NebiusEmbeddings(
        model=settings.nebius.emb_model,
        api_key=api_key_value,
    )
    emb_service = EmbbedingService(emb_model)

    return ContentService(session, emb_service)


def make_graph(config: RunnableConfig | None = None) -> Any:
    content_service = create_content_service()
    AgentServices.initialize(content_service)
    return build_agent_graph()


graph = make_graph
