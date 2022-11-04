from datetime import date, datetime
from typing import List, Optional

from fastapi import Query
from app.schemas.medicine import MedicinesResponse
from app.schemas.pond import PondsResponse
from app.schemas.medicine import MedicinesResponse
from app.schemas.unit import UnitResponse
from app.core.schemal import FilterBase
from app.schemas.specification import SpecificationResponse

from pydantic import BaseModel, Field


class MedicineInCreate(BaseModel):
    medicine_id: int
    amount: int
    adopt_area_id: int
    unit_id: int = None
    specification_id: int = None
    in_date: date
    mfg_date: datetime = None
    exp_date: datetime = None

    class Config:
        orm_mode = True


class MedicineInUpdateRequest(BaseModel):
    amount: int
    unit_id: int = None
    in_date: date = None
    mfg_date: datetime = None
    exp_date: datetime = None

    class Config:
        orm_mode = True


class MedicineInResponse(BaseModel):
    id: int
    batch_code: str
    medicine_id: int
    adopt_area_id: int
    quantity: float
    inventory: float
    unit_id: int = None
    specification_id: int = None
    mfg_date: datetime = None
    exp_date: datetime = None
    created_at: datetime
    in_date: date
    unit: UnitResponse = None
    medicine: MedicinesResponse = None
    specification: SpecificationResponse = None

    class Config:
        orm_mode = True


class MedicineInFilter(FilterBase):
    medicine_id: int = Query(...)
    adopt_area_id: int = Query(...)
    out_of_inventory: bool = Query(False)
    from_date: Optional[datetime] = Query(None)
    to_date: Optional[datetime] = Query(None)

    class Config:
        orm_mode = True

