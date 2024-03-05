from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.role_schema import RoleCreate, RoleOut
from app.crud.role_repository import RoleRepository
from app.core.database import get_async_session
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/roles/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(role_create: RoleCreate, db: AsyncSession = Depends(get_async_session)):
    role_repo = RoleRepository(db)
    role = await role_repo.create_role(role_create)
    return role


@router.get("/roles/", response_model=List[RoleOut])
async def read_roles(db: AsyncSession = Depends(get_async_session)):
    role_repo = RoleRepository(db)
    roles = await role_repo.get_all()
    return roles

@router.get("/roles/{role_id}", response_model=RoleOut)
async def read_role(role_id: int, db: AsyncSession = Depends(get_async_session)):
    role_repo = RoleRepository(db)
    role = await role_repo.get_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role

@router.put("/roles/{role_id}", response_model=RoleOut)
async def update_role(role_id: int, role_data: RoleCreate, db: AsyncSession = Depends(get_async_session)):
    role_repo = RoleRepository(db)
    role = await role_repo.update(role_id, role_data)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role

@router.delete("/roles/{role_id}", response_model=RoleOut)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_async_session)):
    role_repo = RoleRepository(db)
    role = await role_repo.delete(role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role

