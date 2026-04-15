import json
import re
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.agent.config import agent_settings
from src.agent.constants import SEARCH_SYSTEM_PROMPT
from src.agent.services import get_services
from src.agent.state import AgentState, EvaluationResult


def parse_json_from_response(content: str) -> EvaluationResult:
    """Parse JSON from LLM response."""
    content = content.strip()

    json_match = re.search(r"\{[^}]+\}", content)
    if json_match:
        try:
            data = json.loads(json_match.group())
            return EvaluationResult(relevant_ids=data.get("relevant_ids", []))
        except json.JSONDecodeError:
            pass

    ids_match = re.search(r'"relevant_ids"\s*:\s*\[([^\]]+)\]', content)
    if ids_match:
        ids_str = ids_match.group(1)
        ids = [int(x.strip()) for x in ids_str.split(",") if x.strip().isdigit()]
        return EvaluationResult(relevant_ids=ids)

    return EvaluationResult(relevant_ids=[])


async def search_node(state: AgentState) -> dict[str, Any]:
    services = get_services()
    search_tool = await services.get_search_tool()

    query = state.get("query") or state["messages"][-1].content
    limit = agent_settings.default_search_limit

    search_results_raw: str = await search_tool.ainvoke(
        {
            "query": query,
            "limit": limit,
        }
    )

    search_results = []
    for line in search_results_raw.split("---"):
        if "ID:" in line and "Resumen:" in line:
            parts = line.split("\n")
            id_part = parts[0].replace("ID:", "").strip()
            summary_part = parts[1].replace("Resumen:", "").strip()
            try:
                search_results.append(
                    {
                        "id": int(id_part),
                        "summary": summary_part,
                    }
                )
            except ValueError:
                continue

    if not search_results:
        return {
            "search_results": [],
            "evaluation_result": EvaluationResult(relevant_ids=[]),
        }

    contents_str = "\n\n".join([f"ID: {r['id']}\nResumen: {r['summary']}" for r in search_results])

    from langchain_nebius import ChatNebius

    chat_model = ChatNebius(model=agent_settings.model.name)

    evaluation_messages = [
        SystemMessage(
            content=SEARCH_SYSTEM_PROMPT.format(
                university=agent_settings.university_name,
                query=query,
                contents=contents_str,
            )
        ),
        HumanMessage(
            content='¿Cuáles de estos contenidos son relevantes? Responde solo con JSON: {"relevant_ids": [1, 2, 3]}'
        ),
    ]

    response = await chat_model.ainvoke(evaluation_messages)
    evaluation_result = parse_json_from_response(str(response.content))

    return {
        "search_results": search_results,
        "evaluation_result": evaluation_result,
        "query": query,
    }
