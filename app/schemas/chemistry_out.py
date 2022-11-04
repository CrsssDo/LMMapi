from datetime import date, datetime
from typing import List, Optional
from fastapi import Query
from app.schemas.chemistry_in import ChemistryInResponse
from app.schemas.pond import PondsResponse
from app.core.schemal import FilterBase

from pydantic import BaseModel, Field


class ChemistryOutCreate(BaseModel):
    chemistry_in_id: int
    quantity: int
    pond_id: int
    in_date: date = None
    note: Optional[str] = None


    class Config:
        orm_mode = True


class ChemistryOutResponse(BaseModel):
    id: int
    chemistry_in_id: int
    quantity: int
    inventory: int
    note: Optional[str] = None
    chemistry_in: ChemistryInResponse = None
    in_date: date = None
    created_at: datetime
    pond: PondsResponse = None

    class Config:
        orm_mode = True


class ChemistryOutFilter(FilterBase):
    chemistry_id: int = Query(None)
    adopt_area_id: int = Query(None)
    pond_id: int = Query(None)
    chemistry_in_id: int = Query(None)
    from_date: datetime = Query(None)
    to_date: datetime = Query(None)

    class Config:
        orm_mode = True

class ChemistryOutHistoryValue(BaseModel):
    id: int
    name: str
    batch_code: str
    quantity: int
    note: str = None

class ChemistryOutHistoryResponse(BaseModel):
    in_date: date = None
    history_datas: List[ChemistryOutHistoryValue] = []

    class Config:
        orm_mode = True


