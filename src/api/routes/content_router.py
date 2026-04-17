from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_content_service
from src.api.routes.schemas import SearchParams, PaginationParams
from src.api.services.content_service import ContentService
from src.db.models.content import ContentCreate, ContentUpdate, ContentRead

router = APIRouter(prefix="/content", tags=["Content"])


@router.post("/", response_model=ContentRead, status_code=status.HTTP_201_CREATED)
async def create_content(
    content_in: ContentCreate,
    content_service: ContentService = Depends(get_content_service),
):
    return await content_service.create_content(content_in)


@router.get("/", response_model=list[ContentRead])
async def read_contents(
    limit: int = PaginationParams.limit,
    offset: int = PaginationParams.offset,
    content_service: ContentService = Depends(get_content_service),
):
    return await content_service.get_all_contents(limit=limit, offset=offset)


@router.get("/search/", response_model=list[ContentRead])
async def search_content(
    q: str = SearchParams.q,
    limit: int = SearchParams.limit,
    offset: int = SearchParams.offset,
    content_service: ContentService = Depends(get_content_service),
):
    return await content_service.search(q, limit, offset)


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
