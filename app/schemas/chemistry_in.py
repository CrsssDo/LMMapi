from datetime import date, datetime
from typing import List, Optional
from fastapi import Form, Query
from app.schemas.chemistry import ChemistryResponse
from app.schemas.unit import UnitResponse
from app.core.schemal import FilterBase
from pydantic import BaseModel, Field
from app.schemas.specification import SpecificationResponse


class ChemistryInCreateRequest(BaseModel):
    chemistry_id: int
    adopt_area_id: int
    amount: int
    unit_id: int = None
    specification_id: int = None
    in_date: date
    mfg_date: datetime = None
    exp_date: datetime = None

    class Config:
        orm_mode = True


class ChemistryInUpdateRequest(BaseModel):
    amount: int
    unit_id: int = None
    in_date: date = None
    mfg_date: datetime = None
    exp_date: datetime = None

    class Config:
        orm_mode = True


class ChemistryInResponse(BaseModel):
    id: int
    batch_code: str
    chemistry_id: int
    adopt_area_id: int
    quantity: int
    inventory: int
    unit_id: int = None
    specification_id: int = None
    in_date: date
    mfg_date: datetime = None
    exp_date: datetime = None
    created_at: datetime
    unit: UnitResponse = None
    chemistry: ChemistryResponse = None
    specification: SpecificationResponse = None


    class Config:
        orm_mode = True


class ChemistryInFilter(FilterBase):
    chemistry_id: int = Query(...)
    adopt_area_id: int = Query(...)
    out_of_inventory: bool = Query(False)
    from_date: Optional[datetime] = Query(None)
    to_date: Optional[datetime] = Query(None)

    class Config:
        orm_mode = True

