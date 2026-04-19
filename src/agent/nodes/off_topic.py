from typing import Any

from langchain_core.messages import SystemMessage

from src.agent.constants import (
    OFFTOPIC_CAPABILITIES_PROMPT,
    OFFTOPIC_GREETING_PROMPT,
    OFFTOPIC_NOT_RELATED_PROMPT,
)
from src.agent.model_factory import get_chat_model
from src.agent.state import AgentState, ResponseContext, RoutingResult
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
    routing = state.get("routing") or RoutingResult(is_relevant=False)
    reason = routing.reason or "not_related"

    llm = get_chat_model(
        provider=settings.agent.model.provider,
        model_name=settings.agent.model.name,
        temperature=settings.agent.model.temperature,
        api_key=settings.agent.model.api_key,
    )

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

    content = response.content
    if isinstance(content, list):
        content = "\n".join(str(c) for c in content if isinstance(c, str))

    response_ctx = state.get("response") or ResponseContext()
    return {
        "response": ResponseContext(
            response=content, relevant_contents=response_ctx.relevant_contents
        ),
        "routing": RoutingResult(is_relevant=False),
    }
