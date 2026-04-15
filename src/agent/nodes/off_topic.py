from langchain_core.messages import SystemMessage

from src.agent.config import agent_settings
from src.agent.constants import OFFTOPIC_SYSTEM_PROMPT
from src.agent.state import AgentState


def create_off_topic_node(llm):
    def off_topic_node(state: AgentState) -> dict:
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

    return off_topic_node
