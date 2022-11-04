from typing import Optional

from datetime import date
from app.schemas.address import AddressLevel1Response
from app.schemas.measure_index import MeasureIndexResponse
from app.schemas.pond import PondsResponse

from pydantic import BaseModel, Field


class WaterDiaryDetailCreateRequest(BaseModel):
    id: int = None
    measure_index_id: int = None
    water_measure_value: Optional[float] = None 

    class Config:
        orm_mode = True


class WaterDiaryDetailResponse(BaseModel):
    id: int
    water_diaries_id: int = None
    measure_index_id: int = None
    water_measure_value: float = None
    status: bool = None
    measure_index: MeasureIndexResponse = None

    class Config:
        orm_mode = True

