from typing import Any

from langchain_core.messages import SystemMessage

from src.agent.constants import INFO_MESSAGES, RESPOND_SYSTEM_PROMPT
from src.agent.state import AgentState
from src.config import settings


async def respond_node(state: AgentState) -> dict[str, Any]:
    from langchain_nebius import ChatNebius

    llm = ChatNebius(
        model=settings.agent.model.name,
        api_key=settings.agent.router_model.api_key,
        temperature=settings.agent.model.temperature,
    )

    relevant_contents = state.get("relevant_contents", [])

    if not relevant_contents:
        return {
            "response": INFO_MESSAGES["no_encontrado"],
            "sources": [],
        }

    context_parts: list[str] = []
    sources: list[dict[str, Any]] = []

    for content in relevant_contents:
        context_parts.append(
            f"Título: {content['title']}\n"
            f"Categoría: {content['category']}\n"
            f"Fecha: {content['post_date']}\n"
            f"Contenido: {content['content']}"
        )
        sources.append(
            {
                "id": content.get("id"),
                "title": content.get("title"),
                "category": content.get("category"),
                "post_date": content.get("post_date"),
            }
        )

    context = "\n\n---\n\n".join(context_parts)

    messages = [
        SystemMessage(
            content=RESPOND_SYSTEM_PROMPT.format(
                university=settings.agent.university_name,
                max_tokens=settings.agent.max_response_tokens,
                context=context,
            )
        ),
        *state["messages"],
    ]

    full_response = ""
    async for chunk in llm.astream(messages):
        if chunk.content and isinstance(chunk.content, str):
            full_response += chunk.content

    return {
        "response": full_response,
        "sources": sources,
        "visited_ids": [],
        "invalid_ids": [],
    }
