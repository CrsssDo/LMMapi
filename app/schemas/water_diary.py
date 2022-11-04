from typing import List, Optional

from datetime import date
from app.schemas.address import AddressLevel1Response
from app.schemas.pond import PondsResponse
from app.schemas.measure_index import MeasureIndexResponse
from app.schemas.water_diary_detail import WaterDiaryDetailResponse
from app.core.schemal import FilterBase

from pydantic import BaseModel, Field


class WaterDiaryCreateRequest(BaseModel):
    pond_id: int = None

    class Config:
        orm_mode = True


class WaterDiaryFilter(FilterBase):
    pond_id: int = None
    adopt_id: int = None
    selected_date: Optional[date] = None

    class Config:
        orm_mode = True


class WaterDiaryCommentCreateRequest(BaseModel):
    comment: Optional[str] = None 

    class Config:
        orm_mode = True


class WaterDiaryResponse(BaseModel):
    id: int = None
    in_date: date = None
    pond_id: int = None
    comment: str = None
    pond: PondsResponse = None
    water_diaries_value: List[WaterDiaryDetailResponse] = []

    class Config:
        orm_mode = True

class MeasuresReportResponse(BaseModel):
    id: int = None
    name: str = None
    value: float = None
    is_over: bool = False

    class Config:
        orm_mode = True


class WaterDiariesReportResponse(BaseModel):
    pond_code: str = None
    pond_id: int = None
    comment: str = None
    measures: List[MeasuresReportResponse] = []

    class Config:
        orm_mode = True