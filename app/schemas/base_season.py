from enum import Enum
from datetime import date, datetime
from typing import List
from app.schemas.base_season_pond import BaseSeasonPondResponse

from pydantic import BaseModel

from app.schemas.pond import PondsResponse

class BaseSeasonStatus(str, Enum):
    new = 'Mới'
    cancel = 'Đã hủy'
    activating = 'Đang nuôi'
    completed = 'Hoàn thành'


class BaseSeasonCreateRequest(BaseModel):
    pond_list: List = []
    notes: str = None
    adopt_area_id: int = None
    expected_start_date: date = None
    expected_end_date: date = None

    class Config:
        orm_mode = True
        use_enum_values = True


class BaseSeasonResponse(BaseModel):
    id: int
    code: str
    notes: str = None
    adopt_area_id: int = None
    expected_start_date: datetime = None
    expected_end_date: datetime = None
    status: str = None
    base_season_ponds: List[BaseSeasonPondResponse] = []

    class Config:
        orm_mode = True
        use_enum_values = True

class BaseSeasonPondResponse(BaseModel):
    id: int = None
    pond_name: str = None
    status: str = None

class BaseSeasonListResponse(BaseModel):
    id: int
    code: str
    adopt_area_id: int = None
    expected_start_date: datetime = None
    expected_end_date: datetime = None
    status: str = None
    ponds: List[BaseSeasonPondResponse] = [] 

    class Config:
        orm_mode = True
        use_enum_values = True