from typing import List, Optional
from datetime import date
from app.schemas.address import AddressLevel1Response
from app.schemas.measure_index import MeasureIndexResponse
from app.schemas.pond import PondsResponse

from pydantic import BaseModel, Field


class WaterIndexSeasonCreateRequest(BaseModel):
    base_season_pond_id: int = None

    class Config:
        orm_mode = True


class WaterIndexSeasonUpdateRequest(BaseModel):
    id: int
    measure_index_id: int = None
    water_measure_value: Optional[float] = None 

    class Config:
        orm_mode = True

class WaterIndexValueResponse(BaseModel):
    id: int = None
    base_season_pond_id: int = None
    measure_index_id: int = None
    water_measure_value: float = None
    status: bool = None
    measure_indexes: MeasureIndexResponse = None

    class Config:
        orm_mode = True

class WaterIndexSeasonResponse(BaseModel):
    id: int = None
    water_index_poison: str = None
    water_indexes: List[WaterIndexValueResponse] = []

    class Config:
        orm_mode = True

