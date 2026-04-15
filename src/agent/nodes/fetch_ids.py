from src.agent.state import AgentState


def create_fetch_ids_node(content_service):
    async def fetch_ids_node(state: AgentState) -> dict:
        evaluation_result = state.get("evaluation_result")
        if not evaluation_result or not evaluation_result.relevant_ids:
            return {
                "relevant_contents": [],
            }

        contents = await content_service.get_by_ids(evaluation_result.relevant_ids)

        formatted_contents = [content_service.format_content_for_agent(c) for c in contents]

        return {
            "relevant_contents": formatted_contents,
        }

    return fetch_ids_node
