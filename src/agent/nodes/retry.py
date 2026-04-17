from typing import Any

from src.agent.constants import INFO_MESSAGES
from src.agent.state import AgentState
from src.config import settings


async def retry_node(state: AgentState) -> dict[str, Any]:
    retry_count = state.get("retry_count", 0) + 1

    invalid_ids = list(state.get("invalid_ids", []) or [])

    if retry_count >= settings.agent.max_search_retries:
        return {
            "response": INFO_MESSAGES["no_encontrado"],
            "retry_count": retry_count,
            "visited_ids": [],
            "invalid_ids": [],
        }

    return {"retry_count": retry_count, "invalid_ids": invalid_ids}


def should_retry(state: AgentState) -> bool:
    retry_count = state.get("retry_count", 0)
    return retry_count < settings.agent.max_search_retries
