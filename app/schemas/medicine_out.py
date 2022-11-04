from datetime import date, datetime
from typing import List, Optional
from fastapi import Query
from app.schemas.medicine_in import MedicineInResponse
from app.schemas.pond import PondsResponse
from app.core.schemal import FilterBase

from pydantic import BaseModel, Field


class MedicineOutCreate(BaseModel):
    medicine_in_id: int
    quantity: int
    pond_id: int
    in_date: date = None
    note: Optional[str] = None



    class Config:
        orm_mode = True


class MedicineOutResponse(BaseModel):
    id: int
    medicine_in_id: int
    quantity: int
    inventory: int
    note: Optional[str] = None
    in_date: date = None
    medicine_in: MedicineInResponse = None
    created_at: datetime
    pond: PondsResponse = None

    class Config:
        orm_mode = True


class MedicineOutFilter(FilterBase):
    medicine_id: int = Query(None)
    adopt_area_id: int = Query(None)
    pond_id: int = Query(None)
    medicine_in_id: int = Query(None)
    from_date: datetime = Query(None)
    to_date: datetime = Query(None)

    class Config:
        orm_mode = True


class MedicineOutHistoryValue(BaseModel):
    id: int
    name: str
    batch_code: str
    quantity: int
    note: str = None

class MedicineOutHistoryResponse(BaseModel):
    in_date: date = None
    history_datas: List[MedicineOutHistoryValue] = []

    class Config:
        orm_mode = True


