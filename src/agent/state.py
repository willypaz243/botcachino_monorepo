from langgraph.graph import MessagesState
from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    relevant_ids: list[int] = Field(
        default_factory=list,
        description="Lista de IDs de contenido que se consideran relevantes para la consulta",
    )
    no_relevant_ids: list[int] = Field(
        default_factory=list,
        description="Lista de IDs de contenido que se consideran no relevantes para la consulta",
    )


class SearchResultSummary(BaseModel):
    id: int
    summary: str


class AgentState(MessagesState, total=False):
    query: str | None
    original_query: str | None
    is_relevant: bool | None
    off_topic_reason: str | None
    search_results: list[dict[str, str | int]] | None
    evaluation_result: EvaluationResult | None
    retry_count: int
    relevant_contents: list[dict[str, str | int]] | None
    response: str | None
    sources: list[dict[str, str | int | None]] | None
    error: str | None
    visited_ids: list[int] | None
    invalid_ids: list[int] | None
    search_attempts: int | None
