from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.agent.nodes.fetch_ids import fetch_ids_node
from src.agent.nodes.off_topic import off_topic_node
from src.agent.nodes.respond import respond_node
from src.agent.nodes.retry import retry_node
from src.agent.nodes.router import router_node
from src.agent.nodes.search import search_node
from src.agent.state import AgentState


def build_agent_graph() -> CompiledStateGraph[AgentState, None, AgentState, AgentState]:
    checkpointer = InMemorySaver()

    def route_decision(state: AgentState) -> str:
        routing = state.get("routing")

        if routing and not routing.is_relevant:
            return "off_topic"

        response = state.get("response")
        if response and response.relevant_contents:
            if routing and routing.cached_content_useful is True:
                return "respond"
            if routing and routing.cached_content_useful is False:
                return "search"

        return "search"

    def route_search_decision(state: AgentState) -> str:
        evaluation = state.get("evaluation")
        if not evaluation or not evaluation.relevant_ids:
            return "retry"
        return "fetch_ids"

    def route_retry_decision(state: AgentState) -> str:
        search = state.get("search")
        retry_count = search.retry_count if search else 0
        from src.config import settings

        if retry_count >= settings.agent.max_search_retries:
            return "off_topic"
        return "search"

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
                "search": "search",
                "off_topic": "off_topic",
                "respond": "respond",
            },
        )
        .add_conditional_edges(
            "search",
            route_search_decision,
            {
                "fetch_ids": "fetch_ids",
                "retry": "retry",
            },
        )
        .add_edge("fetch_ids", "respond")
        .add_edge("respond", END)
        .add_edge("off_topic", END)
        .add_conditional_edges(
            "retry",
            route_retry_decision,
            {
                "search": "search",
                "off_topic": "off_topic",
            },
        )
        .compile(checkpointer=checkpointer)
    )

    return graph
