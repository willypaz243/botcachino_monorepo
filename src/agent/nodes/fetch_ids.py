from typing import Any

from src.agent.services import get_services
from src.agent.state import AgentState, ResponseContext, SearchContext


async def fetch_ids_node(state: AgentState) -> dict[str, Any]:
    services = get_services()
    content_service = services.get_content_service()

    evaluation = state.get("evaluation")
    search_ctx = state.get("search")
    excluded_ids = set(search_ctx.excluded_ids) if search_ctx else set()

    if evaluation is None or not evaluation.relevant_ids:
        return {
            "response": ResponseContext(),
            "search": SearchContext(excluded_ids=excluded_ids),
        }

    relevant_ids = [id_val for id_val in evaluation.relevant_ids if id_val not in excluded_ids]

    if not relevant_ids:
        return {
            "response": ResponseContext(),
            "search": SearchContext(excluded_ids=excluded_ids),
        }

    contents = await content_service.get_by_ids(relevant_ids)
    formatted_contents = [content_service.format_content_for_agent(c) for c in contents]

    new_excluded = excluded_ids | set(relevant_ids)

    return {
        "response": ResponseContext(relevant_contents=formatted_contents),
        "search": SearchContext(excluded_ids=new_excluded),
    }
