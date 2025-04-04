from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.balance import BalanceCreate, BalanceRead, BalanceUpdate
from app.services.balance_service import BalanceService

router = APIRouter()

@router.post("/", response_model=BalanceRead)
def create_balance(
    balance: BalanceCreate,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: Replace with actual user authentication
):
    return BalanceService.create_balance(db, balance, user_id)

@router.get("/{balance_id}", response_model=BalanceRead)
def get_balance(
    balance_id: int,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: Replace with actual user authentication
):
    balance = BalanceService.get_balance_by_id(db, balance_id, user_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance

@router.get("/", response_model=List[BalanceRead])
def get_all_balances(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    sort_by: str = Query("date", regex="^(name|amount|date|type|category)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: Replace with actual user authentication
):
    return BalanceService.get_all_balances(
        db, user_id, skip, limit, sort_by, sort_order
    )

@router.put("/{balance_id}", response_model=BalanceRead)
def update_balance(
    balance_id: int,
    balance_update: BalanceUpdate,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: Replace with actual user authentication
):
    balance = BalanceService.update_balance(db, balance_id, balance_update, user_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance

@router.delete("/{balance_id}")
def delete_balance(
    balance_id: int,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: Replace with actual user authentication
):
    success = BalanceService.delete_balance(db, balance_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Balance not found")
    return {"message": "Balance deleted successfully"} 