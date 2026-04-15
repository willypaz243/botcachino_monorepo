from typing import AsyncIterator

from langchain_core.messages import HumanMessage
from langgraph.types import StreamMode

from src.agent.graph import build_agent_graph
from src.agent.tools import create_search_tool
from src.agent.constants import INFO_MESSAGES
from src.api.services.content_service import ContentService


class UniversityAgent:
    def __init__(self, content_service: ContentService):
        self.content_service = content_service
        self._graph = None
        self._search_tool = None

    def _get_graph(self):
        if self._graph is None:
            self._search_tool = create_search_tool(self.content_service)
            self._graph = build_agent_graph(
                self.content_service,
                self._search_tool,
            )
        return self._graph

    async def astream_events(
        self,
        message: str,
        thread_id: str,
    ) -> AsyncIterator[dict]:
        graph = self._get_graph()
        config = {"configurable": {"thread_id": thread_id}}

        input_data = {
            "messages": [HumanMessage(content=message)],
            "retry_count": 0,
        }

        yield {"event": "info", "content": INFO_MESSAGES["inicio"]}

        try:
            async for event in graph.astream(
                input_data,
                config,
                stream_mode=StreamMode.Values,
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

    async def invoke(self, message: str, thread_id: str) -> dict:
        graph = self._get_graph()
        config = {"configurable": {"thread_id": thread_id}}

        input_data = {
            "messages": [HumanMessage(content=message)],
            "retry_count": 0,
        }

        result = await graph.ainvoke(input_data, config)

        return {
            "response": result.get("response", ""),
            "sources": result.get("sources", []),
        }
