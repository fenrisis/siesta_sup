from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    name: str
    phone: str
    telegram_id: int
    telegram_name: str


class UserCreate(UserBase):
    role_id: Optional[int] = None


class UserUpdate(UserBase):
    role_id: Optional[int] = None


class UserOut(UserBase):
    id: int
    role_id: int

    class Config:
        from_attributes = True
