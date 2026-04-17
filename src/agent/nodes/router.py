import json
from typing import Any

from langchain_core.messages import SystemMessage

from src.agent.constants import ROUTER_SYSTEM_PROMPT
from src.agent.services import get_services
from src.agent.state import AgentState
from src.config import settings


async def router_node(state: AgentState) -> dict[str, Any]:
    services = get_services()
    await services.get_search_tool()

    from langchain_nebius import ChatNebius

    llm = ChatNebius(
        model=settings.agent.router_model.name,
        api_key=settings.agent.router_model.api_key,
        temperature=settings.agent.router_model.temperature,
    )

    messages = [
        SystemMessage(
            content=ROUTER_SYSTEM_PROMPT.format(university=settings.agent.university_name)
        ),
        *state["messages"][-3:],
    ]

    response = await llm.ainvoke(messages)
    content = str(response.content).strip()

    try:
        result = json.loads(content)
        classification = result.get("classification", "off_topic")
        reason = result.get("reason")
        is_relevant = classification == "relevant"
    except (json.JSONDecodeError, KeyError):
        is_relevant = "relevant" in content.lower()
        reason = "not_related" if not is_relevant else None

    return {
        "is_relevant": is_relevant,
        "off_topic_reason": reason,
    }
