from typing import Optional

from datetime import date
from app.core.schemal import FilterBase

from pydantic import BaseModel, Field


class DeadFishDiaryFilter(FilterBase):
    pond_id: int = None
    adopt_id: int = None
    selected_date: Optional[date] = None

    class Config:
        orm_mode = True


class DeadFishDiaryCreateRequest(BaseModel):
    pond_id: int = None

    class Config:
        orm_mode = True


class DeadFishDiaryUpdateRequest(BaseModel):
    quantity: int = None
    mass: float = None
    average_weight: float = None
    health_condition: str = None

    class Config:
        orm_mode = True

class DeadFishDiaryPondRespone(BaseModel):
    id: int = None
    code: str = None

    class Config:
        orm_mode = True

class DeadFishDiaryResponse(BaseModel):
    id: int = None
    in_date: date = None
    pond_id: int = None
    quantity: int = None
    mass: float = None
    reason: str = None
    average_weight: float = None
    accumulated_loss: int = None
    accumulated_exist: int = None
    estimated_volume: int = None
    health_condition: str = None
    pond: DeadFishDiaryPondRespone = None

    class Config:
        orm_mode = True


class DeadFishDiariesReportResponse(BaseModel):
    id: int = None
    pond_code: str = None
    pond_id: int = None
    quantity: str = None
    reason: str = None

    class Config:
        orm_mode = True