from langchain_core.messages import HumanMessage, SystemMessage

from src.agent.config import agent_settings
from src.agent.constants import SEARCH_SYSTEM_PROMPT
from src.agent.state import AgentState, EvaluationResult


def create_search_node(llm, search_tool, content_service):
    async def search_node(state: AgentState) -> dict:
        query = state.get("query") or state["messages"][-1].content
        limit = agent_settings.default_search_limit

        search_results_raw = await search_tool.ainvoke(
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

        contents_str = "\n\n".join(
            [f"ID: {r['id']}\nResumen: {r['summary']}" for r in search_results]
        )

        evaluation_messages = [
            SystemMessage(
                content=SEARCH_SYSTEM_PROMPT.format(
                    university=agent_settings.university_name,
                    query=query,
                    contents=contents_str,
                )
            ),
            HumanMessage(content="¿Cuáles de estos contenidos son relevantes?"),
        ]

        evaluation_result_raw = await llm.with_structured_output(EvaluationResult).invoke(
            evaluation_messages
        )

        return {
            "search_results": search_results,
            "evaluation_result": evaluation_result_raw,
            "query": query,
        }

    return search_node
