from datetime import datetime
from typing import Optional
from app.schemas.adopt import AdoptAreaWaterEnviroment
from app.schemas.unit import UnitResponse

from pydantic import BaseModel, Field


class MeasureIndexCreateRequest(BaseModel):
    code: str = Field(..., min_length=1)
    max_range: float = Field(None)
    min_range: float = Field(None)
    water_environment: AdoptAreaWaterEnviroment = None
    status: bool = True
    unit_id: int = Field(None)

    class Config:
        orm_mode = True

class MeasureIndexUpdateStatusRequest(BaseModel):
    status: Optional[bool]

    class Config:
        orm_mode = True

class MeasureIndexResponse(BaseModel):
    id: int
    code: str 
    max_range: float = None
    min_range: float = None
    water_environment: str
    unit_id: int = None
    status: bool
    deleted_at: datetime = None
    unit: UnitResponse = None

    class Config:
        orm_mode = True
