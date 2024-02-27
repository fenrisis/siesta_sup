from typing import List, Optional
from sqlalchemy import select
from app.crud.base import BaseRepository
from app.models.models import Role
from app.schemas.role_schema import RoleCreate
from sqlalchemy.ext.asyncio import AsyncSession

class RoleRepository(BaseRepository[Role]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Role)

    async def create_role(self, role_create: RoleCreate) -> Role:
        role = Role(**role_create.dict())
        self.db_session.add(role)  # Correct usage
        await self.db_session.commit()  # Correct usage
        await self.db_session.refresh(role)  # Correct usage
        return role

    async def get_all(self) -> List[Role]:
        query = select(Role)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, role_id: int) -> Optional[Role]:
        role = await self.db_session.get(Role, role_id)
        return role

    async def update(self, role_id: int, role_data: RoleCreate) -> Optional[Role]:
        role = await self.db_session.get(Role, role_id)
        if role:
            for key, value in role_data.dict(exclude_unset=True).items():
                setattr(role, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(role)
            return role
        return None

    async def delete(self, role_id: int) -> Optional[Role]:
        role = await self.db_session.get(Role, role_id)
        if role:
            await self.db_session.delete(role)
            await self.db_session.commit()
            return role
        return None
