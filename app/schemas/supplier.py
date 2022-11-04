from datetime import datetime
from typing import Optional
from app.schemas.address import AddressLevel1Response

from pydantic import BaseModel, Field


class SuppliersTypeResponse(BaseModel):
    id: int
    name: Optional[str] = None

    class Config:
        orm_mode = True


class SupplierUpdateRequest(BaseModel):
    address: str = Field(..., min_length=3, max_length=100)
    name: str = None
    address_level_1_id: int = None
    supplier_type_id: int = None


class SupplierCreateRequest(BaseModel):
    address: str = Field(..., min_length=3, max_length=100)
    name: str = None
    supplier_code: Optional[str] = None
    address_level_1_id: int = None
    supplier_type_id: int = None

    class Config:
        orm_mode = True


class SupplierResponse(BaseModel):
    id: int
    name: str = None
    supplier_code: str = None
    address: str = None
    address_level_1_id: int = None
    supplier_type_id: int = None
    deleted_at: datetime = None
    supplier_type: SuppliersTypeResponse = None
    address_level_1: AddressLevel1Response = None

    class Config:
        orm_mode = True

