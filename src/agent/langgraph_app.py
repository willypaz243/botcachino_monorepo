from typing import Any

from langchain_nebius import NebiusEmbeddings
from langchain_core.runnables import RunnableConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.agent.graph import build_agent_graph
from src.agent.tools import create_search_tool
from src.api.services.content_service import ContentService
from src.api.services.embedding_service import EmbbedingService
from src.config import settings


async def _get_content_service() -> ContentService:
    engine = create_async_engine(
        str(settings.database.url),
        echo=False,
    )
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session = async_session()

    emb_model = NebiusEmbeddings(
        model=settings.nebius.emb_model,
        api_key=settings.nebius.api_key.get_secret_value() if settings.nebius.api_key else None,
    )
    emb_service = EmbbedingService(emb_model)

    return ContentService(session, emb_service)


async def _build_graph() -> Any:
    content_service = await _get_content_service()
    search_tool = await create_search_tool(content_service)
    return build_agent_graph(content_service, search_tool)


_graph_cache: Any | None = None


async def get_graph() -> Any:
    global _graph_cache
    if _graph_cache is None:
        _graph_cache = await _build_graph()
    return _graph_cache


def graph(config: RunnableConfig | None = None) -> Any:
    import asyncio

    return asyncio.run(get_graph())
