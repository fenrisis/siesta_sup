from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sup_schema import SupCreate, SupUpdate, SupOut
from app.crud.sup_repository import SupRepository
from app.core.database import get_async_session
from fastapi import File, UploadFile, Form

router = APIRouter()

@router.post("/sups/", response_model=SupOut, status_code=status.HTTP_201_CREATED)
async def create_sup(
    name: str = Form(...),
    price: int = Form(...),
    quantity: int = Form(...),
    picture: UploadFile = File(None),  # Optional file upload
    db: AsyncSession = Depends(get_async_session)
):
    sup_create = SupCreate(name=name, price=price, quantity=quantity, picture=picture)
    sup_repo = SupRepository(db)
    sup = await sup_repo.create_sup(sup_create)
    return sup

@router.get("/sups/", response_model=List[SupOut])
async def read_sups(db: AsyncSession = Depends(get_async_session)):
    sup_repo = SupRepository(db)
    sups = await sup_repo.get_all_sups()
    return sups

@router.get("/sups/{sup_id}", response_model=SupOut)
async def read_sup(sup_id: int, db: AsyncSession = Depends(get_async_session)):
    sup_repo = SupRepository(db)
    sup = await sup_repo.get_sup_by_id(sup_id)
    if sup is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sup not found")
    return sup

@router.put("/sups/{sup_id}", response_model=SupOut)
async def update_sup(sup_id: int, sup_update: SupUpdate, db: AsyncSession = Depends(get_async_session)):
    sup_repo = SupRepository(db)
    sup = await sup_repo.update_sup(sup_id, sup_update)
    if sup is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sup not found")
    return sup

@router.delete("/sups/{sup_id}", response_model=SupOut)
async def delete_sup(sup_id: int, db: AsyncSession = Depends(get_async_session)):
    sup_repo = SupRepository(db)
    sup = await sup_repo.delete_sup(sup_id)
    if sup is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sup not found")
    return sup