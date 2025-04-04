from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from datetime import datetime

from app.models.sql.balance import BalanceModel
from app.models.schemas import BalanceCreate, BalanceUpdate, Balance

class BalanceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_balance(self, balance: BalanceCreate) -> Balance:
        """
        Crea un nuovo bilancio nel database.
        """
        try:
            db_balance = BalanceModel(
                name=balance.name,
                date=balance.date,
                financial_data=balance.financial_data
            )
            self.db.add(db_balance)
            await self.db.commit()
            await self.db.refresh(db_balance)
            return Balance.from_orm(db_balance)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Errore durante la creazione del bilancio: {str(e)}"
            )

    async def get_balance_by_id(self, balance_id: int) -> Optional[Balance]:
        """
        Recupera un bilancio dal database tramite ID.
        """
        try:
            query = select(BalanceModel).filter(BalanceModel.id == balance_id)
            result = await self.db.execute(query)
            db_balance = result.scalar_one_or_none()
            if db_balance is None:
                return None
            return Balance.from_orm(db_balance)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Errore durante il recupero del bilancio: {str(e)}"
            )

    async def get_all_balances(self, skip: int = 0, limit: int = 100) -> List[Balance]:
        """
        Recupera tutti i bilanci dal database con paginazione.
        """
        try:
            query = select(BalanceModel).offset(skip).limit(limit)
            result = await self.db.execute(query)
            db_balances = result.scalars().all()
            return [Balance.from_orm(balance) for balance in db_balances]
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Errore durante il recupero dei bilanci: {str(e)}"
            )

    async def update_balance(self, balance_id: int, balance_update: BalanceUpdate) -> Optional[Balance]:
        """
        Aggiorna un bilancio esistente nel database.
        """
        try:
            query = select(BalanceModel).filter(BalanceModel.id == balance_id)
            result = await self.db.execute(query)
            db_balance = result.scalar_one_or_none()
            if db_balance is None:
                return None
            
            update_data = balance_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_balance, key, value)
            
            db_balance.updated_at = datetime.now()
            await self.db.commit()
            await self.db.refresh(db_balance)
            return Balance.from_orm(db_balance)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Errore durante l'aggiornamento del bilancio: {str(e)}"
            )

    async def delete_balance(self, balance_id: int) -> bool:
        """
        Elimina un bilancio dal database.
        """
        try:
            query = select(BalanceModel).filter(BalanceModel.id == balance_id)
            result = await self.db.execute(query)
            db_balance = result.scalar_one_or_none()
            if db_balance is None:
                return False
            
            await self.db.delete(db_balance)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Errore durante l'eliminazione del bilancio: {str(e)}"
            ) 