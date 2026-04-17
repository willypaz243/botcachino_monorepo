from typing import Any

from src.agent.services import get_services
from src.agent.state import AgentState


async def fetch_ids_node(state: AgentState) -> dict[str, Any]:
    services = get_services()
    content_service = services.get_content_service()

    evaluation_result = state.get("evaluation_result")
    visited_ids = set(state.get("visited_ids", []) or [])

    if evaluation_result is None or not evaluation_result.relevant_ids:
        return {"relevant_contents": []}

    relevant_ids = [
        id_val for id_val in evaluation_result.relevant_ids if id_val not in visited_ids
    ]

    if not relevant_ids:
        return {"relevant_contents": []}

    contents = await content_service.get_by_ids(relevant_ids)

    formatted_contents = [content_service.format_content_for_agent(c) for c in contents]

    new_visited = list(visited_ids | set(relevant_ids))

    return {
        "relevant_contents": formatted_contents,
        "visited_ids": new_visited,
    }
