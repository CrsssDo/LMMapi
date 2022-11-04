from datetime import datetime
from typing import  Optional
from app.schemas.address import AddressLevel1Response

from pydantic import BaseModel, Field

class PurchasingDealerCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = None
    address: str = Field(..., min_length=1, max_length=255)
    address_level_1_id: int

    class Config:
        orm_mode = True

class PurchasingDealerUpdateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1, max_length=255)
    address_level_1_id: int

    class Config:
        orm_mode = True


class PurchasingDealersResponse(BaseModel):
    id: int = None
    name: str = None
    code: str = None
    address: str = None
    deleted_at: datetime = None
    address_level_1_id: int = None
    address_level_1: AddressLevel1Response = None

    class Config:
        orm_mode = True