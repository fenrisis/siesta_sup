from pydantic import BaseModel, HttpUrl
from typing import Optional


class SupBase(BaseModel):
    name: str
    price: int
    quantity: int


class SupCreate(SupBase):
    picture: Optional[HttpUrl] = None


class SupUpdate(SupBase):
    picture: Optional[HttpUrl] = None


class SupOut(SupBase):
    id: int
    picture: HttpUrl

    class Config:
        from_attributes = True
