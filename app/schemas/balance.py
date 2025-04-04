from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BalanceBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: float
    type: str = Field(..., pattern="^(income|expense)$")
    category: Optional[str] = None

class BalanceCreate(BalanceBase):
    pass

class BalanceUpdate(BalanceBase):
    name: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = Field(None, pattern="^(income|expense)$")

class BalanceRead(BalanceBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True 