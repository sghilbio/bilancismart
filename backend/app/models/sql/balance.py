from sqlalchemy import Column, Integer, String, Date, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class BalanceModel(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    financial_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Balance {self.name} ({self.date})>" 