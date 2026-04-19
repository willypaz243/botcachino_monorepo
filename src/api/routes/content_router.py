from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_content_service
from src.api.schemas import FilterParams, PaginationParams, SearchParams, SortField, SortOrder
from src.api.services.content_service import ContentService
from src.db.models.content import Category, ContentCreate, ContentRead, ContentUpdate

router = APIRouter(prefix="/content", tags=["Content"])


@router.post("/", response_model=ContentRead, status_code=status.HTTP_201_CREATED)
async def create_content(
    content_in: ContentCreate,
    content_service: ContentService = Depends(get_content_service),
):
    return await content_service.create_content(content_in)


@router.get("/", response_model=list[ContentRead])
async def read_contents(
    categories: list[Category] | None = FilterParams.categories,
    start_date: datetime | None = FilterParams.start_date,
    end_date: datetime | None = FilterParams.end_date,
    title_contains: str | None = FilterParams.title_contains,
    summary_contains: str | None = FilterParams.summary_contains,
    content_contains: str | None = FilterParams.content_contains,
    limit: int = PaginationParams.limit,
    offset: int = PaginationParams.offset,
    sort: SortField = PaginationParams.sort,
    order: SortOrder = PaginationParams.order,
    content_service: ContentService = Depends(get_content_service),
):
    return await content_service.get_all_contents(
        categories=categories,
        start_date=start_date,
        end_date=end_date,
        title_contains=title_contains,
        summary_contains=summary_contains,
        content_contains=content_contains,
        limit=limit,
        offset=offset,
        sort_field=sort,
        sort_order=order,
    )


@router.get("/search/", response_model=list[ContentRead])
async def search_content(
    q: str = SearchParams.q,
    limit: int = SearchParams.limit,
    offset: int = SearchParams.offset,
    start_date: datetime | None = SearchParams.start_date,
    end_date: datetime | None = SearchParams.end_date,
    content_service: ContentService = Depends(get_content_service),
):
    return await content_service.search(
        q,
        limit,
        offset,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/{content_id}", response_model=ContentRead)
async def read_content(
    content_id: int,
    content_service: ContentService = Depends(get_content_service),
):
    content = await content_service.get_content_by_id(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.patch("/{content_id}", response_model=ContentRead)
async def update_content(
    content_id: int,
    content_in: ContentUpdate,
    content_service: ContentService = Depends(get_content_service),
):
    content = await content_service.update_content(content_id, content_in)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: int,
    content_service: ContentService = Depends(get_content_service),
):
    success = await content_service.delete_content(content_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content not found")
    return None
