from datetime import date, datetime
from typing import List, Optional
from app.core.schemal import FilterBase

from fastapi import Query

from app.schemas.pond import PondsResponse
from app.schemas.food_in import FoodInResponse

from pydantic import BaseModel


class FoodOutCreateRequest(BaseModel):
    food_in_id: int
    quantity: int
    pond_id: int
    in_date: date = None
    note: Optional[str] = None


    class Config:
        orm_mode = True

class FoodOutFilter(FilterBase):
    food_id: int = Query(None)
    adopt_area_id: int = Query(None)
    pond_id: int = Query(None)
    food_in_id: int = Query(None)
    from_date: datetime = Query(None)
    to_date: datetime = Query(None)

    class Config:
        orm_mode = True


class FoodOutResponse(BaseModel):
    id: int
    food_in_id: int
    quantity: int
    inventory: int
    created_at: datetime
    in_date: date = None
    food_in: FoodInResponse = None
    note: Optional[str] = None
    pond: PondsResponse = None

    class Config:
        orm_mode = True

class FoodOutHistoryValue(BaseModel):
    id: int
    name: str
    batch_code: str
    quantity: int
    note: str = None
    in_date: datetime = None

class FoodOutHistoryResponse(BaseModel):
    in_date: date = None
    history_datas: List[FoodOutHistoryValue] = []

    class Config:
        orm_mode = True




