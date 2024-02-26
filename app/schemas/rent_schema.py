from pydantic import BaseModel
from datetime import datetime


class RentBase(BaseModel):
    rent_start: datetime
    rent_end: datetime


class RentCreate(RentBase):
    user_id: int
    sup_id: int


class RentOut(RentBase):
    id: int
    user_id: int
    sup_id: int

    class Config:
        from_attributes = True
