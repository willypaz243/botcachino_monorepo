import logging
import traceback
import uuid as uuid_module
from collections.abc import AsyncIterator
from typing import Any, cast

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from src.agent.constants import INFO_MESSAGES, RETRY_MESSAGES
from src.agent.graph import build_agent_graph
from src.agent.services import AgentServices
from src.agent.state import AgentState, ResponseContext, SearchContext
from src.api.services.content_service import ContentService
from src.api.services.history_service import HistoryService
from src.db.models.history import ConversationCreate, ConversationUpdate, MessageCreate, Role

logger = logging.getLogger(__name__)


class UniversityAgent:
    def __init__(
        self,
        content_service: ContentService,
        history_service: HistoryService | None = None,
    ) -> None:
        self.content_service = content_service
        self.history_service = history_service
        self._graph: CompiledStateGraph[AgentState, None, AgentState, AgentState] | None = None

    def _get_graph(self):
        if self._graph is None:
            AgentServices.initialize(self.content_service)
            self._graph = build_agent_graph()
        return self._graph

    async def load_history(self, thread_id: str) -> list[HumanMessage | AIMessage]:
        if not self.history_service or not thread_id:
            return []

        conversation = await self.history_service.get_conversation_by_uuid(thread_id)
        if not conversation:
            return []

        messages = await self.history_service.get_messages(
            thread_id,
            limit=50,
        )

        result: list[HumanMessage | AIMessage] = []
        for msg in messages:
            langchain_msg = (
                HumanMessage(content=msg.content, id=str(msg.uuid))
                if msg.role == Role.USER
                else AIMessage(content=msg.content, id=str(msg.uuid))
            )
            result.append(langchain_msg)

        return result

    async def _save_conversation(
        self,
        thread_id: str,
        user_message: str,
        bot_response: str,
    ) -> None:
        if not self.history_service or not thread_id:
            return

        conversation = await self.history_service.get_conversation_by_uuid(thread_id)
        if not conversation:
            title = " ".join(user_message.strip().split()[:5]) or "Nueva conversación"
            conversation = await self.history_service.create_conversation(
                ConversationCreate(title=title),
            )

        await self.history_service.add_message(
            str(conversation.uuid),
            MessageCreate(role=Role.USER, content=user_message),
        )
        await self.history_service.add_message(
            str(conversation.uuid),
            MessageCreate(role=Role.BOT, content=bot_response),
        )

        if not conversation.title or conversation.title == "Nueva conversación":
            await self.history_service.update_conversation(
                str(conversation.uuid),
                ConversationUpdate(
                    title=(" ".join(user_message.strip().split()[:5]) or conversation.title),
                ),
            )

    async def astream_events(
        self,
        message: str,
        thread_id: str,
    ) -> AsyncIterator[dict[str, Any]]:
        if not thread_id or thread_id.strip() == "":
            thread_id = str(uuid_module.uuid4())

        history_messages = await self.load_history(thread_id)

        graph = self._get_graph()
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

        input_messages = list(history_messages) + [HumanMessage(content=message)]

        input_data = cast(
            AgentState,
            {
                "messages": input_messages,
                "search": SearchContext(retry_count=0, excluded_ids=set()),
            },
        )

        bot_response = ""

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
                                content = msg_chunk.content
                                if isinstance(content, str):
                                    bot_response += content
                                else:
                                    for part in content:
                                        if isinstance(part, str):
                                            bot_response += part
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
                                retry_count = 0
                                if isinstance(node_state, dict):
                                    search_context = node_state.get("search", {})
                                    retry_count = getattr(search_context, "retry_count", 0)
                                message_index = min(retry_count, len(RETRY_MESSAGES) - 1)
                                yield {
                                    "event": "info",
                                    "content": RETRY_MESSAGES[message_index],
                                }

        except Exception:
            traceback.print_exc()
            yield {
                "event": "error",
                "content": "Error inesperado",
            }

        await self._save_conversation(thread_id, message, bot_response)

        yield {"event": "done", "content": ""}

    async def invoke(self, message: str, thread_id: str) -> dict[str, Any]:
        graph = self._get_graph()
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

        input_data: AgentState = {
            "messages": [HumanMessage(content=message)],
            "search": SearchContext(retry_count=0, excluded_ids=set()),
        }

        result = await graph.ainvoke(input_data, config)

        response_ctx = result.get("response") or ResponseContext()
        return {
            "response": response_ctx.response or "",
            "sources": response_ctx.sources or [],
        }
