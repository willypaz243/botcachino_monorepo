import json
from typing import Any

from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field, model_validator

from src.agent.constants import ROUTER_SYSTEM_PROMPT
from src.agent.model_factory import get_chat_model
from src.agent.services import get_services
from src.agent.state import AgentState, RoutingResult
from src.config import settings


class RouterOutput(BaseModel):
    classification: str = Field(
        description='Classification: "search" to send to search, "off_topic" for greetings/capabilities/unrelated'
    )
    reason: str | None = Field(
        default=None,
        description='Reason for off_topic: "greeting", "capabilities", or "not_related"',
    )
    cached_content_useful: bool | None = Field(
        default=None,
        description="Whether the cached content from previous queries is useful for the current question. True if cached content can help answer, false if a new search is needed.",
    )

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data = {k.lower(): v for k, v in data.items()}
            classification = data.get("classification", "")
            if isinstance(classification, str):
                lower = classification.lower().strip()
                if lower in ("search", "relevant", "yes", "true", "si", "s"):
                    data["classification"] = "search"
                elif lower in (
                    "off_topic",
                    "irrelevant",
                    "no",
                    "false",
                    "no_relevante",
                    "fuera_de_tema",
                ):
                    data["classification"] = "off_topic"
                else:
                    data["classification"] = "off_topic"
                if data.get("reason") is None and data["classification"] == "off_topic":
                    data["reason"] = "not_related"
        return data


def _parse_from_text(content: str) -> tuple[str, str | None]:
    content = content.strip()
    try:
        result = json.loads(content)
        classification = result.get("classification", "off_topic")
        reason = result.get("reason")
    except (json.JSONDecodeError, AttributeError):
        classification = "search" if "search" in content.lower() else "off_topic"
        reason = "not_related" if classification == "off_topic" else None
    return classification, reason


async def router_node(state: AgentState) -> dict[str, Any]:
    services = get_services()
    await services.get_search_tool()

    llm = get_chat_model(model_config=settings.agent.router_model).with_structured_output(
        RouterOutput
    )

    response = state.get("response")
    has_content = bool(response and response.relevant_contents)

    cached_content_str = ""
    if has_content:
        cached = response.relevant_contents if response else []
        cached_content_str = (
            "Contenido cached disponible (evalúa si es útil para la consulta actual):\n"
        )
        for i, c in enumerate(cached[:5], 1):
            cached_content_str += f"{i}. [{c.get('category', '')}] {c.get('title', '')} (ID: {c.get('id', '')})\n   {c.get('content', '')[:200]}\n\n"

    messages = [
        SystemMessage(
            content=ROUTER_SYSTEM_PROMPT.format(
                university=settings.agent.university_name, cached_content=cached_content_str
            )
        ),
        *state["messages"][-6:],
    ]

    result: RouterOutput | None = await llm.ainvoke(messages)  # type: ignore

    if result is not None:
        is_relevant = result.classification == "search"
        reason = result.reason if result.classification == "off_topic" else None
    else:
        raw_content = str(state["messages"][-1].content).strip()
        classification, reason = _parse_from_text(raw_content)
        is_relevant = classification == "search"

    return {
        "routing": RoutingResult(
            is_relevant=is_relevant,
            reason=reason,
            has_content=has_content,
            cached_content_useful=result.cached_content_useful if result else None,
        ),
    }
