from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.models.schemas import Balance, BalanceCreate, BalanceUpdate
from app.services.balance_service import BalanceService

router = APIRouter()

@router.post("/", response_model=Balance, status_code=status.HTTP_201_CREATED)
async def create_balance(
    balance: BalanceCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuovo bilancio.
    """
    balance_service = BalanceService(db)
    return await balance_service.create_balance(balance)

@router.get("/{balance_id}", response_model=Balance)
async def get_balance(
    balance_id: int,
    db: Session = Depends(get_db)
):
    """
    Recupera un bilancio specifico tramite ID.
    """
    balance_service = BalanceService(db)
    balance = await balance_service.get_balance_by_id(balance_id)
    if balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bilancio con ID {balance_id} non trovato"
        )
    return balance

@router.get("/", response_model=List[Balance])
async def get_all_balances(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Recupera tutti i bilanci con paginazione.
    """
    balance_service = BalanceService(db)
    return await balance_service.get_all_balances(skip=skip, limit=limit)

@router.put("/{balance_id}", response_model=Balance)
async def update_balance(
    balance_id: int,
    balance_update: BalanceUpdate,
    db: Session = Depends(get_db)
):
    """
    Aggiorna un bilancio esistente.
    """
    balance_service = BalanceService(db)
    balance = await balance_service.update_balance(balance_id, balance_update)
    if balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bilancio con ID {balance_id} non trovato"
        )
    return balance

@router.delete("/{balance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_balance(
    balance_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un bilancio.
    """
    balance_service = BalanceService(db)
    success = await balance_service.delete_balance(balance_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bilancio con ID {balance_id} non trovato"
        )
    return None 