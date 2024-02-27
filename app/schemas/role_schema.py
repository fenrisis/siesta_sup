from pydantic.types import Json
from pydantic import BaseModel
from typing import Optional, Dict, Any

class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    permissions: Optional[Json] = None


class RoleOut(BaseModel):
    id: int
    name: str
    permissions: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "name": "admin",
                "permissions": {"create": True, "update": True, "delete": True}
            }
        }