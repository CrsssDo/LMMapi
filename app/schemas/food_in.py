from datetime import date, datetime
from typing import List, Optional

from fastapi import Form, Query
from app.schemas.food import FoodResponse
from app.core.schemal import FilterBase
from app.schemas.specification import SpecificationResponse
from pydantic import BaseModel, Field


class FoodInCreateRequest(BaseModel):
    food_id: int
    adopt_area_id: int
    amount: int
    type_code: int
    specification_id: int
    in_date: date
    mfg_date: datetime = None
    exp_date: datetime = None

    class Config:
        orm_mode = True

class FoodInUpdateRequest(BaseModel):
    amount: int
    type_code: int
    in_date: date = None
    mfg_date: datetime = None
    exp_date: datetime = None

    class Config:
        orm_mode = True


class FoodInResponse(BaseModel):
    id: int
    batch_code: str
    food_id: int
    adopt_area_id: int
    quantity: int
    inventory: int
    type_code: int
    specification_id: int = None
    in_date: date
    mfg_date: datetime = None
    exp_date: datetime = None
    created_at: datetime
    food: FoodResponse = None
    specification: SpecificationResponse = None


    class Config:
        orm_mode = True


class FoodInFilter(FilterBase):
    food_id: int = Query(...)
    adopt_area_id: int = Query(...)
    out_of_inventory: bool = Query(False)
    from_date: Optional[datetime] = Query(None)
    to_date: Optional[datetime] = Query(None)

    class Config:
        orm_mode = True

