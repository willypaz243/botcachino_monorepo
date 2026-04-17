import logging
from collections.abc import AsyncIterator
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from src.agent.constants import INFO_MESSAGES, RETRY_MESSAGES
from src.agent.graph import build_agent_graph
from src.agent.services import AgentServices
from src.agent.state import AgentState
from src.api.services.content_service import ContentService

logger = logging.getLogger(__name__)


class UniversityAgent:
    def __init__(self, content_service: ContentService) -> None:
        self.content_service = content_service
        self._graph: CompiledStateGraph[AgentState, None, AgentState, AgentState] | None = None

    def _get_graph(self):
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
            "visited_ids": [],
            "invalid_ids": [],
        }

        yield {"event": "info", "content": INFO_MESSAGES["inicio"]}

        try:
            async for event in graph.astream(
                input_data,
                config,
                stream_mode=["updates", "messages"],
                version="v2",
            ):
                part_type = event.get("type") if isinstance(event, dict) else None

                if part_type == "messages":
                    data = event.get("data")
                    if isinstance(data, tuple) and len(data) >= 2:
                        msg_chunk, meta = data
                        langgraph_node = (
                            meta.get("langgraph_node") if isinstance(meta, dict) else None
                        )
                        if langgraph_node in ("respond", "off_topic"):
                            if hasattr(msg_chunk, "content") and msg_chunk.content:
                                yield {"event": "text", "content": msg_chunk.content}
                elif part_type == "updates":
                    data = event.get("data")
                    if isinstance(data, dict):
                        for node_name, node_state in data.items():
                            if not isinstance(node_name, str):
                                continue
                            if node_name == "router":
                                yield {"event": "info", "content": INFO_MESSAGES["analizar"]}
                            elif node_name == "search":
                                yield {"event": "info", "content": INFO_MESSAGES["buscar"]}
                            elif node_name == "evaluation":
                                yield {"event": "info", "content": INFO_MESSAGES["evaluar"]}
                            elif node_name == "fetch_ids":
                                yield {"event": "info", "content": INFO_MESSAGES["recuperar"]}
                            elif node_name == "respond":
                                yield {"event": "info", "content": INFO_MESSAGES["generar"]}
                            elif node_name == "retry":
                                retry_count = (
                                    node_state.get("retry_count", 0)
                                    if isinstance(node_state, dict)
                                    else 0
                                )
                                message_index = min(retry_count, len(RETRY_MESSAGES) - 1)
                                yield {
                                    "event": "info",
                                    "content": RETRY_MESSAGES[message_index],
                                }

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
            "visited_ids": [],
            "invalid_ids": [],
        }

        result = await graph.ainvoke(input_data, config)

        return {
            "response": result.get("response", ""),
            "sources": result.get("sources", []),
        }
