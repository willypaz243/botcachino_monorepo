from typing import Any

from langgraph.graph import MessagesState
from pydantic import BaseModel, Field, field_serializer, model_validator


class RoutingResult(BaseModel):
    is_relevant: bool
    reason: str | None = None
    has_content: bool = False
    cached_content_useful: bool | None = None


class SearchContext(BaseModel):
    query: str | None = None
    retry_count: int = 0
    excluded_ids: set[int] = Field(default_factory=set)

    @field_serializer("excluded_ids")
    def _serialize_excluded_ids(self, v: set[int]) -> list[int]:
        return list(v)

    @model_validator(mode="before")
    @classmethod
    def _deserialize_excluded_ids(cls, data: Any) -> Any:
        if isinstance(data, dict) and "excluded_ids" in data:
            data = dict(data)
            if isinstance(data["excluded_ids"], list):
                data["excluded_ids"] = set(data["excluded_ids"])
        return data


class EvaluationContext(BaseModel):
    relevant_ids: list[int] = Field(default_factory=list)
    no_relevant_ids: list[int] = Field(default_factory=list)


class ResponseContext(BaseModel):
    response: str | None = None
    sources: list[dict] = Field(default_factory=list)
    relevant_contents: list[dict] = Field(default_factory=list)


class AgentState(MessagesState, total=False):
    routing: RoutingResult | None
    search: SearchContext
    evaluation: EvaluationContext | None
    response: ResponseContext
