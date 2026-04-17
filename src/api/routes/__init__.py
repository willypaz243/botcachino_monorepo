from fastapi import APIRouter

from .content_router import router as content_router
from .agent_router import router as agent_router
from .history_router import router as history_router

api_router = APIRouter(prefix="/api")

api_router.include_router(content_router)
api_router.include_router(agent_router)
api_router.include_router(history_router)
