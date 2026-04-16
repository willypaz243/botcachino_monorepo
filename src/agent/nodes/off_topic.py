from typing import Any

from langchain_core.messages import SystemMessage

from src.agent.constants import OFFTOPIC_SYSTEM_PROMPT
from src.agent.state import AgentState
from src.config import settings


def off_topic_node(state: AgentState) -> dict[str, Any]:
    from langchain_nebius import ChatNebius

    llm = ChatNebius(
        model=settings.agent.model.name,
        api_key=settings.agent.router_model.api_key,
        temperature=settings.agent.model.temperature,
    )

    messages = [
        SystemMessage(
            content=OFFTOPIC_SYSTEM_PROMPT.format(university=settings.agent.university_name)
        ),
    ]

    response = llm.invoke(messages)

    return {
        "response": response.content,
        "is_relevant": False,
    }
