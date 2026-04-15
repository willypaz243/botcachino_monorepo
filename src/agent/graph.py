from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from src.agent.state import AgentState
from src.agent.nodes.router import router_node
from src.agent.nodes.search import search_node
from src.agent.nodes.off_topic import off_topic_node
from src.agent.nodes.fetch_ids import fetch_ids_node
from src.agent.nodes.respond import respond_node
from src.agent.nodes.retry import retry_node, should_retry


def build_agent_graph():
    checkpointer = InMemorySaver()

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
