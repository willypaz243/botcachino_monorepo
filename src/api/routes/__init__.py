from fastapi import APIRouter

from .content_router import router as content_router

api_router = APIRouter(prefix="/api")

api_router.include_router(content_router)
