from typing import Any

from src.agent.constants import INFO_MESSAGES
from src.agent.state import AgentState, ResponseContext, SearchContext
from src.config import settings


async def retry_node(state: AgentState) -> dict[str, Any]:
    search_ctx = state.get("search") or SearchContext()
    retry_count = search_ctx.retry_count + 1

    if retry_count >= settings.agent.max_search_retries:
        response_ctx = state.get("response") or ResponseContext()
        return {
            "response": ResponseContext(
                response=INFO_MESSAGES["no_encontrado"],
                relevant_contents=response_ctx.relevant_contents,
            ),
            "search": SearchContext(retry_count=retry_count),
        }

    return {
        "search": SearchContext(retry_count=retry_count, excluded_ids=set(search_ctx.excluded_ids))
    }
