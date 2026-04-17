from typing import Any

from src.agent.state import AgentState, EvaluationResult
from src.config import settings


async def evaluation_node(state: AgentState) -> dict[str, Any]:
    """Evalúa si los resultados son suficientes para responder"""

    evaluation_result = state.get("evaluation_result")
    if not evaluation_result:
        return {"evaluation_result": EvaluationResult(relevant_ids=[])}

    relevant_ids = evaluation_result.relevant_ids
    limit = settings.agent.default_search_limit

    return {
        "evaluation_result": evaluation_result,
    }


def should_fetch_ids(state: AgentState) -> bool:
    """Determina si hay suficientes IDs relevantes para fetch_ids"""
    evaluation_result = state.get("evaluation_result")
    if not evaluation_result:
        return False

    relevant_ids = evaluation_result.relevant_ids
    return len(relevant_ids) > 0


def should_retry_search(state: AgentState) -> bool:
    """Determina si se debe hacer retry de búsqueda"""
    evaluation_result = state.get("evaluation_result")
    retry_count = state.get("retry_count", 0)

    if retry_count >= settings.agent.max_search_retries:
        return False

    if not evaluation_result:
        return True

    relevant_ids = evaluation_result.relevant_ids
    return len(relevant_ids) == 0
