from typing import Optional, List
from sqlalchemy import select
from app.crud.base import BaseRepository
from app.models.models import Sup
from app.schemas.sup_schema import SupCreate, SupUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
import shutil
from pathlib import Path


class SupRepository(BaseRepository[Sup]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Sup)

    async def create_sup(self, sup_create: SupCreate) -> Sup:
        # If an image is uploaded, save it to the 'sup_images' directory
        if sup_create.picture:
            image_path = Path('media/sup_images') / sup_create.picture.filename
            image_path.parent.mkdir(parents=True, exist_ok=True)  # Create directory if doesn't exist
            with image_path.open('wb') as buffer:
                shutil.copyfileobj(sup_create.picture.file, buffer)
            image_url = f'/media/sup_images/{image_path.name}'  # Relative URL for accessing the image
        else:
            image_url = None

        # Create Sup with image URL
        sup_data = sup_create.dict()
        sup_data['picture'] = image_url
        sup = Sup(**sup_data)
        self.db_session.add(sup)
        await self.db_session.commit()
        await self.db_session.refresh(sup)
        return sup

    async def update_sup(self, sup_id: int, sup_update: SupUpdate) -> Sup:
        sup = await self.db_session.get(Sup, sup_id)  # Correct usage
        if not sup:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sup not found")
        for var, value in sup_update.dict(exclude_unset=True).items():
            setattr(sup, var, value) if value is not None else None
        await self.db_session.commit()  # Correct usage
        await self.db_session.refresh(sup)  # Correct usage
        return sup

    async def get_sup_by_id(self, sup_id: int) -> Optional[Sup]:
        return await self.db_session.get(Sup, sup_id)  # Correct usage

    async def get_all_sups(self) -> List[Sup]:
        query = select(Sup)
        result = await self.db_session.execute(query)  # Correct usage
        return result.scalars().all()

    async def delete_sup(self, sup_id: int) -> Optional[Sup]:
        sup = await self.db_session.get(Sup, sup_id)  # Correct usage
        if not sup:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sup not found")
        await self.db_session.delete(sup)  # Correct usage
        await self.db_session.commit()  # Correct usage
        return sup

