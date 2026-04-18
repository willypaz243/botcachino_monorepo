from datetime import datetime
from enum import Enum

from fastapi import Query


class SortField(str, Enum):
    """Campos permitidos para ordenamiento. Valida contra inyecciones."""

    POST_DATE = "post_date"
    TITLE = "title"
    CATEGORY = "category"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class SortOrder(str, Enum):
    """Dirección del ordenamiento."""

    ASC = "asc"
    DESC = "desc"


class SortParams:
    sort = Query(
        default=SortField.POST_DATE,
        title="Sort field",
        description=(
            "Field to sort results by. "
            "Allowed values: post_date, title, category, created_at, updated_at."
        ),
        examples=["post_date", "title", "created_at"],
    )

    order = Query(
        default=SortOrder.DESC,
        title="Sort order",
        description="Sort direction: 'asc' for ascending, 'desc' for descending.",
        examples=["asc", "desc"],
    )


class PaginationParams:
    limit = Query(
        default=50,
        title="Result limit",
        description="Maximum number of results to return.",
        ge=1,
        le=100,
        examples=[10, 50, 100],
    )

    offset = Query(
        default=0,
        title="Offset",
        description="Number of results to skip for pagination.",
        ge=0,
        examples=[0, 10, 50],
    )

    sort = SortParams.sort
    order = SortParams.order


class DateFilterParams:
    start_date: datetime | None = Query(
        default=None,
        title="Start date",
        description="Filter content published on or after this date (ISO 8601 format).",
        examples=["2025-01-01T00:00:00", "2025-06-15"],
    )

    end_date: datetime | None = Query(
        default=None,
        title="End date",
        description="Filter content published on or before this date (ISO 8601 format).",
        examples=["2025-12-31T23:59:59", "2025-06-30"],
    )


class FilterParams:
    categories = Query(
        default=None,
        title="Categories",
        description="List of categories to filter by."
    )
    start_date = DateFilterParams.start_date
    end_date = DateFilterParams.end_date
    title_contains = Query(
        default=None,
        title="Title contains",
        description="Filter by title contents."
    )
    summary_contains = Query(
        default=None,
        title="Summary contains",
        description="Filter by summary contents."
    )
    content_contains = Query(
        default=None,
        title="Content contains",
        description="Filter by main body contents."
    )


class SearchParams:
    q = Query(
        ...,
        title="Search query",
        description="The text query to search for semantically similar content.",
        min_length=1,
        max_length=500,
        examples=["scholarship opportunities", "latest news about technology"],
    )

    limit = Query(
        default=5,
        title="Result limit",
        description="Maximum number of results to return, ordered by best semantic match.",
        ge=1,
        le=100,
        examples=[5, 10, 20],
    )

    offset = PaginationParams.offset

    start_date = DateFilterParams.start_date
    end_date = DateFilterParams.end_date
