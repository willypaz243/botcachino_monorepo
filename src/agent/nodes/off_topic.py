from typing import Any

from langchain_core.messages import SystemMessage

from src.agent.config import agent_settings
from src.agent.constants import OFFTOPIC_SYSTEM_PROMPT
from src.agent.state import AgentState


def off_topic_node(state: AgentState) -> dict[str, Any]:
    from langchain_nebius import ChatNebius

    llm = ChatNebius(
        model=agent_settings.model.name,
        temperature=agent_settings.model.temperature,
    )

    messages = [
        SystemMessage(
            content=OFFTOPIC_SYSTEM_PROMPT.format(university=agent_settings.university_name)
        ),
    ]

    response = llm.invoke(messages)

    return {
        "response": response.content,
        "is_relevant": False,
    }
