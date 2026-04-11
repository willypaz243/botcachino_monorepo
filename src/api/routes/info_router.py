from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_info_service
from src.api.services.info_service import InfoService
from src.db.models.info import InfoCreate, InfoRead, InfoUpdate

info_router = APIRouter(prefix="/info")


@info_router.get("/", response_model=List[InfoRead])
async def list_info(
    skip: int = 0, limit: int = 100, service: InfoService = Depends(get_info_service)
):
    """Obtener lista de información"""
    return await service.list_info(skip=skip, limit=limit)


@info_router.get("/{info_id}", response_model=InfoRead)
async def get_info(info_id: int, service: InfoService = Depends(get_info_service)):
    """Obtener información por ID"""
    info = await service.get_info(info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Info not found")
    return info


@info_router.post("/", response_model=InfoRead)
async def create_info(
    info: InfoCreate, service: InfoService = Depends(get_info_service)
):
    """Crear nueva información"""
    return await service.create_info(info)


@info_router.put("/{info_id}", response_model=InfoRead)
async def update_info(
    info_id: int,
    info_update: InfoUpdate,
    service: InfoService = Depends(get_info_service),
):
    """Actualizar información por ID"""
    updated_info = await service.update_info(info_id, info_update)
    if not updated_info:
        raise HTTPException(status_code=404, detail="Info not found")
    return updated_info


@info_router.delete("/{info_id}")
async def delete_info(info_id: int, service: InfoService = Depends(get_info_service)):
    """Eliminar información por ID"""
    success = await service.delete_info(info_id)
    if not success:
        raise HTTPException(status_code=404, detail="Info not found")
    return {"message": "Info deleted successfully"}
