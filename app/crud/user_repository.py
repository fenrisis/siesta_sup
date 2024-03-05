from typing import Optional
from sqlalchemy import select
from app.crud.base import BaseRepository
from app.models.models import User
from app.schemas.user_schema import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(BaseRepository[User]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, User)

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(**user_create.dict())
        self.db_session.add(user)  # Use `self.db_session` directly
        await self.db_session.commit()  # Commit changes asynchronously
        await self.db_session.refresh(user)  # Refresh instance to get new values
        return user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        user = await self.db_session.get(User, user_id)
        if not user:
            return None  # User not found
        for var, value in user_update.dict(exclude_unset=True).items():
            setattr(user, var, value) if value is not None else None
        await self.db_session.commit()  # Commit changes asynchronously
        await self.db_session.refresh(user)  # Refresh instance
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.db_session.get(User, user_id)
        if user:
            await self.db_session.delete(user)  # Correctly awaited
            await self.db_session.commit()
            return True
        return False

    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await self.db_session.execute(query)  # Execute query asynchronously
        return result.scalars().first()
