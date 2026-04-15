from langchain_core.messages import SystemMessage

from src.agent.config import agent_settings
from src.agent.constants import ROUTER_SYSTEM_PROMPT
from src.agent.state import AgentState


def create_router_node(llm):
    def router_node(state: AgentState) -> dict:
        messages = [
            SystemMessage(
                content=ROUTER_SYSTEM_PROMPT.format(university=agent_settings.university_name)
            ),
            *state["messages"][-3:],
        ]

        result = llm.with_structured_output({"relevant": bool, "off_topic": bool}).invoke(messages)

        is_relevant = result.get("relevant", False)

        return {
            "is_relevant": is_relevant,
        }

    return router_node
