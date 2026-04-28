from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.agent.constants import SEARCH_SYSTEM_PROMPT, SEARCH_TOOL_PROMPT
from src.agent.model_factory import get_chat_model
from src.agent.services import get_services
from src.agent.state import AgentState, EvaluationContext, SearchContext
from src.config import settings


async def search_node(state: AgentState) -> dict[str, Any]:
    services = get_services()
    search_tool = await services.get_search_tool()

    tools = {"semantic_search": search_tool}

    search_ctx = state.get("search") or SearchContext()

    raw_query = state["messages"][-1].content
    original_query = raw_query if isinstance(raw_query, str) else str(raw_query)
    excluded_ids = set(search_ctx.excluded_ids)

    llm_with_tools = get_chat_model(
        model_config=settings.agent.router_model, temperature_override=0.3
    ).bind_tools([search_tool])

    search_messages = [
        SystemMessage(
            content=SEARCH_TOOL_PROMPT.format(
                university=settings.agent.university_name,
                query=original_query,
            )
        ),
        *state["messages"][-8:],
    ]

    search_response = await llm_with_tools.ainvoke(search_messages)

    tools_results = ""
    if hasattr(search_response, "tool_calls") and search_response.tool_calls:
        for tool_call in search_response.tool_calls:
            tool = tools.get(tool_call.get("name", "semantic_search"), lambda *_: "")
            result = await tool.ainvoke(tool_call.get("args"))
            tools_results += f"\nTool Name:{tool_call.get('name')}\nArgs: {tool_call.get('args')}\nResults:\n{result}\n"

    if not tools_results:
        return {
            "evaluation": None,
            "search": SearchContext(
                query=original_query,
                retry_count=search_ctx.retry_count,
                excluded_ids=set(excluded_ids),
            ),
        }

    chat_model = get_chat_model(model_config=settings.agent.model, temperature_override=0)
    structured_model = chat_model.with_structured_output(EvaluationContext)

    system_message = SystemMessage(
        content=SEARCH_SYSTEM_PROMPT.format(
            university=settings.agent.university_name,
            query=original_query,
            contents=tools_results,
        )
    )
    human_message = HumanMessage(content="Dame los ids relevantes a la solicitud.")
    messages = [system_message, human_message]

    evaluation_result: EvaluationContext | None = None

    for _ in range(3):
        try:
            evaluation_result = await structured_model.ainvoke(messages)  # type: ignore
            break
        except Exception:
            messages.append(SystemMessage(content="Intenta reformular la búsqueda."))

    if evaluation_result is not None:
        new_excluded = excluded_ids | set(evaluation_result.no_relevant_ids)
        return {
            "evaluation": evaluation_result,
            "search": SearchContext(
                query=original_query,
                retry_count=search_ctx.retry_count,
                excluded_ids=new_excluded,
            ),
        }
    return {}
