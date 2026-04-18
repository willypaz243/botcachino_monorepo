import json
from typing import Any

from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

from src.agent.constants import ROUTER_SYSTEM_PROMPT
from src.agent.services import get_services
from src.config import settings


class RouterClassification(BaseModel):
    classification: str = Field(
        description='Classification: "search" to send to search, "off_topic" for greetings/capabilities/unrelated'
    )
    reason: str | None = Field(
        default=None,
        description='Reason for off_topic: "greeting", "capabilities", or "not_related"',
    )


def _parse_from_text(content: str) -> tuple[bool, str | None]:
    content = content.strip()
    try:
        result = json.loads(content)
        classification = result.get("classification", "off_topic")
        reason = result.get("reason")
        is_relevant = classification == "search"
    except (json.JSONDecodeError, AttributeError):
        is_relevant = "search" in content.lower()
        reason = "not_related" if not is_relevant else None
    return is_relevant, reason


async def router_node(state: dict[str, Any]) -> dict[str, Any]:
    services = get_services()
    await services.get_search_tool()

    from langchain_nebius import ChatNebius

    llm = ChatNebius(
        model=settings.agent.router_model.name,
        api_key=settings.agent.router_model.api_key,
        temperature=settings.agent.router_model.temperature,
    ).with_structured_output(RouterClassification)

    messages = [
        SystemMessage(
            content=ROUTER_SYSTEM_PROMPT.format(university=settings.agent.university_name)
        ),
        *state["messages"][-6:],
    ]

    result: RouterClassification | None = await llm.ainvoke(messages)  # type: ignore

    if result is not None:
        is_relevant = result.classification == "search"
        reason = result.reason if result.classification == "off_topic" else None
    else:
        raw_content = str(state["messages"][-1].content).strip()
        is_relevant, reason = _parse_from_text(raw_content)

    return {
        "is_relevant": is_relevant,
        "off_topic_reason": reason,
    }
