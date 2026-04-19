from typing import Any

from src.agent.state import AgentState, EvaluationContext
from src.config import settings


async def evaluation_node(state: AgentState) -> dict[str, Any]:
    """Evalúa si los resultados son suficientes para responder"""

    evaluation = state.get("evaluation")
    if not evaluation:
        return {"evaluation": EvaluationContext(relevant_ids=[])}

    return {
        "evaluation": evaluation,
    }


def should_fetch_ids(state: AgentState) -> bool:
    """Determina si hay suficientes IDs relevantes para fetch_ids"""
    evaluation = state.get("evaluation")
    if not evaluation:
        return False

    relevant_ids = evaluation.relevant_ids
    return len(relevant_ids) > 0


def should_retry_search(state: AgentState) -> bool:
    """Determina si se debe hacer retry de búsqueda"""
    evaluation = state.get("evaluation")
    search_ctx = state.get("search")
    retry_count = search_ctx.retry_count if search_ctx else 0

    if retry_count >= settings.agent.max_search_retries:
        return False

    if not evaluation:
        return True

    relevant_ids = evaluation.relevant_ids
    return len(relevant_ids) == 0
