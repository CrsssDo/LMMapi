from typing import List, Optional
from datetime import datetime
from app.schemas.adopt import AdoptResponse
from app.schemas.image import ImagesResponse
from app.schemas.dead_fish_diary import DeadFishDiaryResponse

from pydantic import BaseModel, Field


class PondTypesResponse(BaseModel):
    id: int
    code: str = None
    name: str
    symbol: str = None

    class Config:
        orm_mode = True

class PondTypeCreateRquest(BaseModel):
    name: str
    symbol: str

class PondCategorizesResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class PondsResponse(BaseModel):
    id: int
    code: Optional[str] = None
    area: int = None
    volume: int = None
    location: Optional[str] = None
    pond_map_name: str = None
    adopt_area_id: int = None
    pond_type_id: int = None
    can_rate: bool = False
    number_order: int = None
    pond_map_name: str = None
    base_season_id: int = None
    base_season_status: str = None
    pond_categorize_id: int = None
    finished_date: Optional[datetime] = None
    status: bool = None
    deleted_at: datetime = None
    pond_type: PondTypesResponse = None
    pond_categorize: PondCategorizesResponse = None
    adopt_area: AdoptResponse = None
    dead_fish: List[DeadFishDiaryResponse] = None
    images: List[ImagesResponse] = None


    class Config:
        orm_mode = True

class PondDetailResponse(PondsResponse):
    images: List[ImagesResponse] = None
    

class PondCreateRequest(BaseModel):
    area: int = None
    volume: int = None
    location: Optional[str] = None
    number_order: int = None
    adopt_area_id: int = None
    pond_type_id: int = None
    pond_categorize_id: int = None
    finished_date: Optional[datetime] = None
    status: bool = True

    class Config:
        orm_mode = True


class PondUpdateRequest(BaseModel):
    area: int = None
    volume: int = None
    location: Optional[str] = None
    number_order: int = None
    adopt_area_id: int = None
    pond_type_id: int = None
    pond_categorize_id: int = None
    finished_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class PondStatusUpdateRequest(BaseModel):
    status: Optional[bool]

    class Config:
        orm_mode = True
