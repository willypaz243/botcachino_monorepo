from collections.abc import AsyncIterator
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from src.agent.graph import build_agent_graph
from src.agent.services import AgentServices
from src.agent.constants import INFO_MESSAGES
from src.agent.state import AgentState
from src.api.services.content_service import ContentService


class UniversityAgent:
    def __init__(self, content_service: ContentService) -> None:
        self.content_service = content_service
        self._graph: Any = None

    def _get_graph(self) -> Any:
        if self._graph is None:
            AgentServices.initialize(self.content_service)
            self._graph = build_agent_graph()
        return self._graph

    async def astream_events(
        self,
        message: str,
        thread_id: str,
    ) -> AsyncIterator[dict[str, Any]]:
        graph = self._get_graph()
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

        input_data: AgentState = {
            "messages": [HumanMessage(content=message)],
            "retry_count": 0,
        }

        yield {"event": "info", "content": INFO_MESSAGES["inicio"]}

        try:
            async for event in graph.astream(
                input_data,
                config,
                stream_mode="values",
            ):
                node_name = event.get("_node_name", "")

                if node_name == "router":
                    yield {"event": "info", "content": INFO_MESSAGES["analizar"]}

                elif node_name == "search":
                    yield {"event": "info", "content": INFO_MESSAGES["buscar"]}

                elif node_name == "fetch_ids":
                    yield {"event": "info", "content": INFO_MESSAGES["recuperar"]}

                elif node_name == "respond":
                    response = event.get("response", "")
                    if response:
                        yield {"event": "text", "content": response}
                    yield {"event": "info", "content": INFO_MESSAGES["completado"]}

                elif node_name == "off_topic":
                    response = event.get("response", "")
                    if response:
                        yield {"event": "text", "content": response}
                    yield {"event": "info", "content": INFO_MESSAGES["completado"]}

                elif node_name == "retry":
                    retry_count = event.get("retry_count", 0)
                    if retry_count < 5:
                        yield {"event": "info", "content": INFO_MESSAGES["reintentando"]}

        except Exception as e:
            yield {
                "event": "error",
                "content": f"Error inesperado: {str(e)}",
            }

        yield {"event": "done", "content": ""}

    async def invoke(self, message: str, thread_id: str) -> dict[str, Any]:
        graph = self._get_graph()
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

        input_data: AgentState = {
            "messages": [HumanMessage(content=message)],
            "retry_count": 0,
        }

        result = await graph.ainvoke(input_data, config)

        return {
            "response": result.get("response", ""),
            "sources": result.get("sources", []),
        }
