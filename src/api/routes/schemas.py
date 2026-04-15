from fastapi import Query


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

    offset = Query(
        default=0,
        title="Offset",
        description="Number of results to skip for pagination.",
        ge=0,
        examples=[0, 10, 20],
    )
