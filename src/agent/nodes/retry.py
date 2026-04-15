from src.agent.config import agent_settings
from src.agent.constants import INFO_MESSAGES
from src.agent.state import AgentState


def create_retry_node():
    def retry_node(state: AgentState) -> dict:
        retry_count = state.get("retry_count", 0) + 1

        if retry_count >= agent_settings.max_search_retries:
            return {
                "response": INFO_MESSAGES["no_encontrado"],
                "retry_count": retry_count,
            }

        return {
            "retry_count": retry_count,
        }

    return retry_node


def should_retry(state: AgentState) -> bool:
    evaluation_result = state.get("evaluation_result")
    if not evaluation_result:
        return True

    if not evaluation_result.relevant_ids:
        retry_count = state.get("retry_count", 0)
        return retry_count < agent_settings.max_search_retries

    return False
