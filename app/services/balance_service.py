from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.balance import Balance
from app.schemas.balance import BalanceCreate, BalanceUpdate

class BalanceService:
    @staticmethod
    def create_balance(db: Session, balance: BalanceCreate, user_id: int) -> Balance:
        db_balance = Balance(
            **balance.model_dump(),
            user_id=user_id
        )
        db.add(db_balance)
        db.commit()
        db.refresh(db_balance)
        return db_balance

    @staticmethod
    def get_balance_by_id(db: Session, balance_id: int, user_id: int) -> Optional[Balance]:
        return db.query(Balance).filter(
            Balance.id == balance_id,
            Balance.user_id == user_id
        ).first()

    @staticmethod
    def get_all_balances(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "date",
        sort_order: str = "desc"
    ) -> List[Balance]:
        query = db.query(Balance).filter(Balance.user_id == user_id)
        
        # Apply sorting
        if sort_order.lower() == "desc":
            query = query.order_by(desc(getattr(Balance, sort_by)))
        else:
            query = query.order_by(getattr(Balance, sort_by))
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_balance(
        db: Session,
        balance_id: int,
        balance_update: BalanceUpdate,
        user_id: int
    ) -> Optional[Balance]:
        db_balance = BalanceService.get_balance_by_id(db, balance_id, user_id)
        if not db_balance:
            return None
            
        update_data = balance_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_balance, field, value)
            
        db.commit()
        db.refresh(db_balance)
        return db_balance

    @staticmethod
    def delete_balance(db: Session, balance_id: int, user_id: int) -> bool:
        db_balance = BalanceService.get_balance_by_id(db, balance_id, user_id)
        if not db_balance:
            return False
            
        db.delete(db_balance)
        db.commit()
        return True 