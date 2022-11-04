from datetime import datetime
from typing import  Optional

from pydantic import BaseModel, Field


class UnitUpdateRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=6)
    description: str = Field(..., min_length=3, max_length=255)



class UnitCreateRequest(BaseModel):
    code: str = Field(..., max_length=20)
    description: str = Field(..., max_length=255)

    class Config:
        orm_mode = True


class UnitResponse(BaseModel):
    id: int
    unit_code: str = None
    code: str = None
    description: str = None
    deleted_at: datetime = None

    class Config:
        orm_mode = True