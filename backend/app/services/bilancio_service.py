from typing import List, Optional
from datetime import datetime
from app.models.schemas import BilancioCreate, BilancioUpdate, Bilancio

class BilancioService:
    def __init__(self):
        # TODO: Inizializzare il database
        self.bilanci = []
        self.counter = 0

    async def create_bilancio(self, bilancio: BilancioCreate) -> Bilancio:
        self.counter += 1
        new_bilancio = Bilancio(
            id=self.counter,
            **bilancio.model_dump(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.bilanci.append(new_bilancio)
        return new_bilancio

    async def get_bilancio(self, bilancio_id: int) -> Optional[Bilancio]:
        for bilancio in self.bilanci:
            if bilancio.id == bilancio_id:
                return bilancio
        return None

    async def get_bilanci(self, skip: int = 0, limit: int = 100) -> List[Bilancio]:
        return self.bilanci[skip:skip + limit]

    async def update_bilancio(self, bilancio_id: int, bilancio_update: BilancioUpdate) -> Optional[Bilancio]:
        for i, bilancio in enumerate(self.bilanci):
            if bilancio.id == bilancio_id:
                update_data = bilancio_update.model_dump(exclude_unset=True)
                updated_bilancio = Bilancio(
                    **{**bilancio.model_dump(), **update_data, "updated_at": datetime.now()}
                )
                self.bilanci[i] = updated_bilancio
                return updated_bilancio
        return None

    async def delete_bilancio(self, bilancio_id: int) -> bool:
        for i, bilancio in enumerate(self.bilanci):
            if bilancio.id == bilancio_id:
                self.bilanci.pop(i)
                return True
        return False 