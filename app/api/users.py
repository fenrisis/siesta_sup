from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.openapi.models import Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.crud.user_repository import UserRepository
from app.core.database import get_async_session
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_async_session)):
    user_repo = UserRepository(db)
    user = await user_repo.create_user(user_create)
    return user

@router.get("/users/", response_model=List[UserOut])
async def read_users(db: AsyncSession = Depends(get_async_session)):
    user_repo = UserRepository(db)
    users = await user_repo.get_all()
    return users

@router.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_async_session)):
    user_repo = UserRepository(db)
    user = await user_repo.update_user(user_id, user_data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user_repo = UserRepository(db)
    success = await user_repo.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    # No need to return a JSONResponse or any other body
