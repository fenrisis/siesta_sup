from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Generic, TypeVar, Type, List, Optional

# Define a generic type variable for our repos
T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db_session = db_session
        self.model = model

    async def get_all(self) -> List[T] :
        query = select(self.model)
        result = await self.db_session.execute(query)
        return list(result.scalars().all())  # Convert to list explicitly

    async def get_by_id(self, id: int) -> Optional[T]:
        query = select(self.model).filter(self.model.id == id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def create(self, create_schema) -> T:
        obj = self.model(**create_schema.dict())
        self.db_session.add(obj)
        await self.db_session.commit()
        await self.db_session.refresh(obj)
        return obj

    async def update(self, id: int, update_schema) -> Optional[T]:
        obj = await self.get_by_id(id)
        if obj:
            for var, value in vars(update_schema).items():
                setattr(obj, var, value) if value else None
            await self.db_session.commit()
            await self.db_session.refresh(obj)
        return obj

    async def delete(self, id: int) -> None:
        obj = await self.get_by_id(id)
        if obj:
            self.db_session.delete(obj)
            await self.db_session.commit()