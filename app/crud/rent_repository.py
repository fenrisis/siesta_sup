from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import BaseRepository
from app.models.models import Rent
from app.schemas.rent_schema import RentCreate
from datetime import datetime


class RentRepository(BaseRepository[Rent]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Rent)

    async def create_rent(self, rent_create: RentCreate) -> Rent:
        rent = Rent(**rent_create.dict())
        self.db_session.add(rent)
        await self.db_session.commit()
        await self.db_session.refresh(rent)
        return rent

    async def get_rent_by_id(self, rent_id: int) -> Optional[Rent]:
        # Use `self.db_session.get()` directly for asynchronous operations
        return await self.db_session.get(Rent, rent_id)

    async def get_rents_for_user(self, user_id: int) -> List[Rent]:
        query = select(Rent).where(Rent.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def update_rent(self, rent_id: int, rent_start: datetime, rent_end: datetime) -> Optional[Rent]:
        rent = await self.db_session.get(Rent, rent_id)
        if rent:
            rent.rent_start = rent_start
            rent.rent_end = rent_end
            await self.db_session.commit()
            await self.db_session.refresh(rent)
            return rent
        return None

    async def delete_rent(self, rent_id: int) -> Optional[Rent]:
        rent = await self.db_session.get(Rent, rent_id)
        if rent:
            await self.db_session.delete(rent)
            await self.db_session.commit()
            return rent
        return None
