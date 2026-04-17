from datetime import datetime

from fastapi import Query


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
