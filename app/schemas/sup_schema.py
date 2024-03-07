from pydantic import  HttpUrl
from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional

class SupBase(BaseModel):
    name: str
    price: int
    quantity: int

class SupCreate(SupBase):
    picture: Optional[UploadFile] = None

class SupUpdate(SupBase):
    picture: Optional[UploadFile] = None


class SupUpdate(SupBase):
    picture: Optional[HttpUrl] = None


class SupOut(SupBase):
    id: int
    picture: Optional[str]

    class Config:
        from_attributes = True
