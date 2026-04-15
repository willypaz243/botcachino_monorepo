from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
import operator


class EvaluationResult(BaseModel):
    relevant_ids: list[int] = Field(default_factory=list)


class SearchResultSummary(BaseModel):
    id: int
    summary: str


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    query: str | None
    original_query: str | None
    is_relevant: bool | None
    search_results: list[dict] | None
    evaluation_result: EvaluationResult | None
    retry_count: int
    relevant_contents: list[dict] | None
    response: str | None
    sources: list[dict] | None
    error: str | None
