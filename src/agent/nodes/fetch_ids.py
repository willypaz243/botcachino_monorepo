from typing import Any

from src.agent.state import AgentState
from src.agent.services import get_services


async def fetch_ids_node(state: AgentState) -> dict[str, Any]:
    services = get_services()
    content_service = services.get_content_service()

    evaluation_result = state.get("evaluation_result")
    if not evaluation_result or not evaluation_result.relevant_ids:
        return {"relevant_contents": []}

    contents = await content_service.get_by_ids(evaluation_result.relevant_ids)

    formatted_contents = [content_service.format_content_for_agent(c) for c in contents]

    return {"relevant_contents": formatted_contents}
