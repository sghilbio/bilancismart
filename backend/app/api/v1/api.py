from fastapi import APIRouter
from app.api.v1.endpoints import bilancio, balance, analyze

api_router = APIRouter()

# Qui verranno importati e inclusi i vari router delle API
# from .endpoints import items, users, etc. 

api_router.include_router(bilancio.router, prefix="/bilanci", tags=["bilanci"])
api_router.include_router(balance.router, prefix="/balances", tags=["balances"])
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"]) 