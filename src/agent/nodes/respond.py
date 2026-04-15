from langchain_core.messages import SystemMessage

from src.agent.config import agent_settings
from src.agent.constants import INFO_MESSAGES, RESPOND_SYSTEM_PROMPT
from src.agent.state import AgentState


def create_respond_node(llm):
    def respond_node(state: AgentState) -> dict:
        relevant_contents = state.get("relevant_contents", [])

        if not relevant_contents:
            return {
                "response": INFO_MESSAGES["no_encontrado"],
                "sources": [],
            }

        context_parts = []
        sources = []

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
                    university=agent_settings.university_name,
                    max_tokens=agent_settings.max_response_tokens,
                    context=context,
                )
            ),
            *state["messages"],
        ]

        response = llm.invoke(messages)

        return {
            "response": response.content,
            "sources": sources,
        }

    return respond_node
