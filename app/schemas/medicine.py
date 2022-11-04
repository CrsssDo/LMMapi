from typing import List, Optional
from datetime import datetime
from app.schemas.image import ImagesResponse
from app.schemas.supplier import SupplierResponse
from app.schemas.medicine_type import MedicineTypesResponse

from pydantic import BaseModel, Field


class MedicineCreateRequest(BaseModel):
    receiver_code: Optional[str]
    name: str = Field(...,min_length=2, max_length=255)
    uses: str = Field(...)
    element: str = Field(...)
    instructions_for_use: Optional[str] = None
    supplier_id: int
    medicine_type_id: int
    status: bool = True
    analysed_date: Optional[datetime] = None
    declared_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class MedicinesResponse(BaseModel):
    id: int
    code: str
    receiver_code: str
    name: str
    uses: str
    element: str
    instructions_for_use: str = None
    supplier_id: int
    medicine_type_id: int = None
    status: bool
    analysed_date: datetime = None
    declared_date: datetime = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime = None
    supplier: SupplierResponse = None
    medicine_type: MedicineTypesResponse = None

    class Config:
        orm_mode = True

class MedicineDetailResponse(MedicinesResponse):
    images: List[ImagesResponse] = None


class MedicineUpdateRequest(BaseModel):
    receiver_code: str
    name: str = Field(..., min_length=3, max_length=255)
    uses: str = Field(..., min_length=3)
    element: str = Field(..., min_length=3)
    instructions_for_use: Optional[str] = None
    supplier_id: Optional[int]
    medicine_type_id: int
    analysed_date: Optional[datetime]
    declared_date: Optional[datetime]

    class Config:
        orm_mode = True


class MedicineStatusUpdateRequest(BaseModel):
    status: Optional[bool]

    class Config:
        orm_mode = True

