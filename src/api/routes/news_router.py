from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_news_service
from src.api.services.news_service import NewsService
from src.db.models.news import NewsCreate, NewsRead, NewsUpdate

news_router = APIRouter(prefix="/news")


@news_router.get("/", response_model=List[NewsRead])
async def list_news(
    skip: int = 0, limit: int = 100, service: NewsService = Depends(get_news_service)
):
    """Obtener lista de noticias"""
    return await service.list_news(skip=skip, limit=limit)


@news_router.get("/{news_id}", response_model=NewsRead)
async def get_news(news_id: int, service: NewsService = Depends(get_news_service)):
    """Obtener noticia por ID"""
    news = await service.get_news(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@news_router.post("/", response_model=NewsRead)
async def create_news(
    news: NewsCreate, service: NewsService = Depends(get_news_service)
):
    """Crear nueva noticia"""
    return await service.create_news(news)


@news_router.put("/{news_id}", response_model=NewsRead)
async def update_news(
    news_id: int,
    news_update: NewsUpdate,
    service: NewsService = Depends(get_news_service),
):
    """Actualizar noticia por ID"""
    updated_news = await service.update_news(news_id, news_update)
    if not updated_news:
        raise HTTPException(status_code=404, detail="News not found")
    return updated_news


@news_router.delete("/{news_id}")
async def delete_news(news_id: int, service: NewsService = Depends(get_news_service)):
    """Eliminar noticia por ID"""
    success = await service.delete_news(news_id)
    if not success:
        raise HTTPException(status_code=404, detail="News not found")
    return {"message": "News deleted successfully"}
