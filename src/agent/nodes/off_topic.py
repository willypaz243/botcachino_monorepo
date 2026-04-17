from typing import Any

from langchain_core.messages import SystemMessage

from src.agent.constants import (
    OFFTOPIC_CAPABILITIES_PROMPT,
    OFFTOPIC_GREETING_PROMPT,
    OFFTOPIC_NOT_RELATED_PROMPT,
)
from src.agent.state import AgentState
from src.config import settings
from src.db.models.content import Category


CATEGORY_LABELS: dict[Category, str] = {
    Category.INFO: "Información general",
    Category.NEW: "Noticias",
    Category.SCHOLARSH: "Becas y financiamiento",
    Category.ANN: "Anuncios",
}


def _get_categories_string() -> str:
    """Retorna lista de categorías como string separada por comas."""
    return ", ".join([CATEGORY_LABELS[cat] for cat in Category])


async def off_topic_node(state: AgentState) -> dict[str, Any]:
    from langchain_nebius import ChatNebius

    llm = ChatNebius(
        model=settings.agent.model.name,
        api_key=settings.agent.router_model.api_key,
        temperature=settings.agent.model.temperature,
    )

    reason = state.get("off_topic_reason", "not_related")
    university = settings.agent.university_name
    categories = _get_categories_string()

    if reason == "greeting":
        system_prompt = OFFTOPIC_GREETING_PROMPT.format(
            university=university, categories=categories
        )
    elif reason == "capabilities":
        system_prompt = OFFTOPIC_CAPABILITIES_PROMPT.format(
            university=university, categories=categories
        )
    else:
        system_prompt = OFFTOPIC_NOT_RELATED_PROMPT.format(
            university=university, categories=categories
        )

    messages = [SystemMessage(content=system_prompt)]

    response = await llm.ainvoke(messages)

    return {
        "response": response.content,
        "is_relevant": False,
    }
