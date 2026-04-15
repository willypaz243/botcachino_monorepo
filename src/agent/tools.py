from langchain_core.tools import tool

from src.agent.exceptions import SearchError
from src.api.services.content_service import ContentService


async def create_search_tool(content_service: ContentService):
    @tool(response_format="content")
    async def semantic_search(query: str, limit: int = 5) -> str:
        """Search for relevant content using semantic similarity.

        Args:
            query: The search query to find relevant content.
            limit: Maximum number of results to return (default: 5).

        Returns:
            A formatted string with search results containing id and summary for each item.
        """
        try:
            contents = await content_service.search(query, limit=limit)

            if not contents:
                return "No se encontraron resultados para la búsqueda."

            results = []
            for content in contents:
                summary = await content_service.format_content_summary(content)
                results.append(f"ID: {summary['id']}\nResumen: {summary['summary']}")

            return "\n---\n".join(results)

        except Exception as e:
            raise SearchError(f"Error durante la búsqueda: {str(e)}")

    return semantic_search
