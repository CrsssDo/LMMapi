from typing import List, Optional
from datetime import date
from app.core.schemal import FilterBase
from app.schemas.chemistry import ChemistryResponse
from app.schemas.unit import UnitResponse

from pydantic import BaseModel, Field


class EnvironmentRenovationCreateRequest(BaseModel):
    code: Optional[str] = None
    exp_date: Optional[date] = None
    pond_id: int = None
    quantity: int = None
    chemistry_id: int = None
    unit_id: int = None
    reason: Optional[str] = None

    class Config:
        orm_mode = True


class EnvironmentRenovationResponse(BaseModel):
    id: int = None
    code: Optional[str] = None
    exp_date: Optional[date] = None
    pond_id: int = None
    quantity: int = None
    chemistry_id: int = None
    unit_id: int = None
    reason: Optional[str] = None
    unit: UnitResponse = None
    chemistry: ChemistryResponse = None

    class Config:
        orm_mode = True

class EnvironmentRenovationValue(BaseModel):
    id: int = None
    code: str = None
    chemistry: str = None
    quantity: int = None
    exp_date: date = None
    unit: str = None
    reason: Optional[str] = None

class EnvironmentRenovationHistoryResponse(BaseModel):
    in_date: date = None
    histories: List[EnvironmentRenovationValue] = []

    class Config:
        orm_mode = True
