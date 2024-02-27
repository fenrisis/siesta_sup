from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Generic, TypeVar, Type, List, Optional

# Define a generic type variable for our repos
T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db_session = db_session
        self.model = model

    async def get_all(self) -> List[T]:
        async with self.db_session() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_id(self, id: int) -> Optional[T]:
        async with self.db_session() as session:
            query = select(self.model).filter(self.model.id == id)
            result = await session.execute(query)
            return result.scalars().first()

    async def create(self, create_schema) -> T:
        async with self.db_session() as session:
            obj = self.model(**create_schema.dict())
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def update(self, id: int, update_schema) -> Optional[T]:
        async with self.db_session() as session:
            obj = await self.get_by_id(id)
            if obj:
                for var, value in vars(update_schema).items():
                    setattr(obj, var, value) if value else None
                await session.commit()
                await session.refresh(obj)
            return obj

    async def delete(self, id: int) -> None:
        async with self.db_session() as session:
            obj = await self.get_by_id(id)
            if obj:
                await session.delete(obj)
                await session.commit()