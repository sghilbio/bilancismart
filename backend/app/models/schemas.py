from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, date

class BilancioBase(BaseModel):
    nome: str
    descrizione: Optional[str] = None
    data: datetime
    importo: float
    categoria: str
    tipo: str  # "entrata" o "uscita"

class BilancioCreate(BilancioBase):
    pass

class Bilancio(BilancioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BilancioUpdate(BaseModel):
    nome: Optional[str] = None
    descrizione: Optional[str] = None
    data: Optional[datetime] = None
    importo: Optional[float] = None
    categoria: Optional[str] = None
    tipo: Optional[str] = None

# Nuovi modelli per Balance
class BalanceBase(BaseModel):
    name: str
    date: date
    financial_data: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Bilancio 2024",
                "date": "2024-01-01",
                "financial_data": {
                    "attivo": {
                        "circolante": 100000,
                        "immobilizzazioni": 50000
                    },
                    "passivo": {
                        "debiti": 30000,
                        "patrimonio_netto": 120000
                    }
                }
            }
        }

class BalanceCreate(BalanceBase):
    pass

class BalanceUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[date] = None
    financial_data: Optional[Dict[str, Any]] = None

class Balance(BalanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 