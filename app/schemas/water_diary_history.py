from typing import Optional

from datetime import date, datetime
from app.schemas.address import AddressLevel1Response
from app.schemas.measure_index import MeasureIndexResponse

from pydantic import BaseModel, Field


class WaterDiaryHistoryResponse(BaseModel):
    id: int
    measure_value: float = None
    measure_name: str = None
    in_date: datetime = None

    class Config:
        orm_mode = True

