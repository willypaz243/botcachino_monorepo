from langchain_core.tools import tool

from src.agent.exceptions import SearchError
from src.api.schemas import SortField, SortOrder
from src.api.services.content_service import ContentService
from src.db.models.content import Category


async def create_search_tool(content_service: ContentService):
    @tool(response_format="content")
    async def semantic_search(
        query: str,
        limit: int = 5,
        categories: list[Category] | None = None,
        sort_field: SortField = SortField.POST_DATE,
        sort_order: SortOrder = SortOrder.DESC,
    ) -> str:
        """Search for relevant content using semantic similarity.

        Args:
            query: The search query to find relevant content.
            limit: Maximum number of results to return (default: 5).
            categories: Filter by content category (INFO, NEW, SCHOLARSH, ANN).
            sort_field: Field to sort results by (default: post_date).
            sort_order: Sort direction — 'asc' or 'desc' (default: desc).

        Returns:
            A formatted string with search results containing id and summary for each item.
        """
        try:
            contents = await content_service.search(
                query,
                limit=limit,
                categories=categories,
                sort_field=sort_field,
                sort_order=sort_order,
            )

            if not contents:
                return "No se encontraron resultados para la búsqueda."

            results = []
            for content in contents:
                summary = await content_service.format_content_summary(content)
                results.append(
                    f"ID: {summary['id']}\nTitle: {summary['title']}\nResumen: {summary['summary']}"
                )

            return "\n---\n".join(results)

        except Exception as e:
            raise SearchError(f"Error durante la búsqueda: {str(e)}")

    return semantic_search
