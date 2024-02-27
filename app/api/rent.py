from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.rent_schema import RentCreate, RentOut
from app.crud.rent_repository import RentRepository
from app.core.database import get_async_session

router = APIRouter()

@router.post("/rents/", response_model=RentOut, status_code=status.HTTP_201_CREATED)
async def create_rent(rent_create: RentCreate, db: AsyncSession = Depends(get_async_session)):
    rent_repo = RentRepository(db)
    rent = await rent_repo.create_rent(rent_create)
    return rent

@router.get("/rents/{rent_id}", response_model=RentOut)
async def read_rent(rent_id: int, db: AsyncSession = Depends(get_async_session)):
    rent_repo = RentRepository(db)
    rent = await rent_repo.get_rent_by_id(rent_id)
    if rent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rent not found")
    return rent

@router.get("/rents/user/{user_id}", response_model=List[RentOut])
async def read_rents_for_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    rent_repo = RentRepository(db)
    rents = await rent_repo.get_rents_for_user(user_id)
    return rents

@router.put("/rents/{rent_id}", response_model=RentOut)
async def update_rent(rent_id: int, rent_data: RentCreate, db: AsyncSession = Depends(get_async_session)):  # Use RentUpdate if you have it
    rent_repo = RentRepository(db)
    rent = await rent_repo.update_rent(rent_id, rent_data.rent_start, rent_data.rent_end)  # Adjust if using a different schema for update
    if rent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rent not found")
    return rent

@router.delete("/rents/{rent_id}", response_model=RentOut)
async def delete_rent(rent_id: int, db: AsyncSession = Depends(get_async_session)):
    rent_repo = RentRepository(db)
    rent = await rent_repo.delete_rent(rent_id)
    if rent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rent not found")
    return rent