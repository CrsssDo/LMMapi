from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CleanSeasonCreateRequest(BaseModel):
    base_season_pond_id: int = None

    class Config:
        orm_mode = True


class CleanSeasonCompleteUpdateRequest(BaseModel):
    start_date: datetime 
    finish_date: datetime
    process_description: str
    time_clear_pond: str
    time_between_season: str
    chemical_used: str

    class Config:
        orm_mode = True


class CleanSeasonUpdateRequest(BaseModel):
    start_date: Optional[datetime] = None
    finish_date: Optional[datetime] = None
    process_description: Optional[str] = None
    time_clear_pond: Optional[str] = None
    time_between_season: Optional[str] = None
    chemical_used: Optional[str] = None

    class Config:
        orm_mode = True

class CleanSeasonResponse(BaseModel):
    id: int = None
    start_date: datetime = None
    finish_date: datetime = None
    process_description: str = None
    time_clear_pond: str = None
    time_between_season: str = None
    chemical_used: str = None

    class Config:
        orm_mode = True

