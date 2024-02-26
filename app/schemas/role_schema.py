from pydantic import BaseModel
from pydantic.types import Json
from typing import Optional


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    permissions: Optional[Json] = None


class RoleOut(RoleBase):
    id: int
    permissions: Json

    class Config:
        from_attributes = True
