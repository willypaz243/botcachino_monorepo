from typing import Any

from langchain_core.messages import SystemMessage

from src.agent.config import agent_settings
from src.agent.constants import ROUTER_SYSTEM_PROMPT
from src.agent.services import get_services
from src.agent.state import AgentState


async def router_node(state: AgentState) -> dict[str, Any]:
    services = get_services()
    await services.get_search_tool()

    from langchain_nebius import ChatNebius

    llm = ChatNebius(
        model=agent_settings.router_model.name,
        temperature=agent_settings.router_model.temperature,
    )

    messages = [
        SystemMessage(
            content=ROUTER_SYSTEM_PROMPT.format(university=agent_settings.university_name)
        ),
        *state["messages"][-3:],
    ]

    response = llm.invoke(messages)
    content = str(response.content).lower().strip()

    is_relevant = "relevant" in content and content.count("relevant") >= content.count("off_topic")

    return {
        "is_relevant": is_relevant,
    }
