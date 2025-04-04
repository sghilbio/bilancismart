from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.schemas import Bilancio, BilancioCreate, BilancioUpdate
from app.services.bilancio_service import BilancioService

router = APIRouter()
bilancio_service = BilancioService()

@router.post("/", response_model=Bilancio)
async def create_bilancio(bilancio: BilancioCreate):
    return await bilancio_service.create_bilancio(bilancio)

@router.get("/{bilancio_id}", response_model=Bilancio)
async def get_bilancio(bilancio_id: int):
    bilancio = await bilancio_service.get_bilancio(bilancio_id)
    if bilancio is None:
        raise HTTPException(status_code=404, detail="Bilancio not found")
    return bilancio

@router.get("/", response_model=List[Bilancio])
async def get_bilanci(skip: int = 0, limit: int = 100):
    return await bilancio_service.get_bilanci(skip=skip, limit=limit)

@router.put("/{bilancio_id}", response_model=Bilancio)
async def update_bilancio(bilancio_id: int, bilancio_update: BilancioUpdate):
    bilancio = await bilancio_service.update_bilancio(bilancio_id, bilancio_update)
    if bilancio is None:
        raise HTTPException(status_code=404, detail="Bilancio not found")
    return bilancio

@router.delete("/{bilancio_id}")
async def delete_bilancio(bilancio_id: int):
    success = await bilancio_service.delete_bilancio(bilancio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bilancio not found")
    return {"message": "Bilancio deleted successfully"} 