from typing import Any

from src.agent.tools import create_search_tool
from src.api.services.content_service import ContentService


class AgentServices:
    _content_service: ContentService | None = None
    _search_tool: Any = None

    @classmethod
    def initialize(cls, content_service: ContentService) -> None:
        cls._content_service = content_service

    @classmethod
    def get_content_service(cls) -> ContentService:
        if cls._content_service is None:
            raise RuntimeError("AgentServices not initialized. Call initialize() first.")
        return cls._content_service

    @classmethod
    async def get_search_tool(cls) -> Any:
        if cls._search_tool is None:
            cs = cls.get_content_service()
            cls._search_tool = await create_search_tool(cs)
        return cls._search_tool


def get_services() -> type[AgentServices]:
    return AgentServices
