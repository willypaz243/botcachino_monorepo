from typing import TYPE_CHECKING

from langchain_nebius import ChatNebius
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from src.agent.config import agent_settings
from src.agent.state import AgentState
from src.agent.nodes.router import create_router_node
from src.agent.nodes.search import create_search_node
from src.agent.nodes.off_topic import create_off_topic_node
from src.agent.nodes.fetch_ids import create_fetch_ids_node
from src.agent.nodes.respond import create_respond_node
from src.agent.nodes.retry import create_retry_node, should_retry

if TYPE_CHECKING:
    from src.api.services.content_service import ContentService


def create_chat_model():
    kwargs: dict = {
        "model": agent_settings.model.name,
        "temperature": agent_settings.model.temperature,
    }
    if agent_settings.model.api_key:
        kwargs["api_key"] = agent_settings.model.api_key
    return ChatNebius(**kwargs)


def create_router_model():
    kwargs: dict = {
        "model": agent_settings.router_model.name,
        "temperature": agent_settings.router_model.temperature,
    }
    if agent_settings.router_model.api_key:
        kwargs["api_key"] = agent_settings.router_model.api_key
    return ChatNebius(**kwargs)


def build_agent_graph(
    content_service: "ContentService",
    search_tool,
):
    chat_model = create_chat_model()
    router_model = create_router_model()
    checkpointer = InMemorySaver()

    router_node = create_router_node(router_model)
    search_node = create_search_node(chat_model, search_tool, content_service)
    off_topic_node = create_off_topic_node(chat_model)
    fetch_ids_node = create_fetch_ids_node(content_service)
    respond_node = create_respond_node(chat_model)
    retry_node = create_retry_node()

    def route_decision(state: AgentState) -> str:
        is_relevant = state.get("is_relevant")
        if is_relevant is False:
            return "off_topic"
        return "relevant"

    def route_search_decision(state: AgentState) -> str:
        if should_retry(state):
            return "search"
        return "respond"

    graph = (
        StateGraph(AgentState)
        .add_node("router", router_node)
        .add_node("search", search_node)
        .add_node("off_topic", off_topic_node)
        .add_node("fetch_ids", fetch_ids_node)
        .add_node("respond", respond_node)
        .add_node("retry", retry_node)
        .add_edge(START, "router")
        .add_conditional_edges(
            "router",
            route_decision,
            {
                "relevant": "search",
                "off_topic": "off_topic",
            },
        )
        .add_edge("search", "fetch_ids")
        .add_edge("fetch_ids", "respond")
        .add_edge("respond", END)
        .add_edge("off_topic", END)
        .add_conditional_edges(
            "fetch_ids",
            route_search_decision,
            {
                "search": "search",
                "respond": "respond",
            },
        )
        .compile(checkpointer=checkpointer)
    )

    return graph
