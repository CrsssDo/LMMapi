from datetime import datetime
from typing import Optional
from app.schemas.address import AddressLevel1Response, AddressLevel2Response, AddressLevel3Response
from pydantic import BaseModel, Field
from app.schemas.purchasing_dealer import PurchasingDealersResponse

class CollectSeasonCreateRequest(BaseModel):
    base_season_pond_id: int = None

    class Config:
        orm_mode = True


class CollectSeasonUpdateRequest(BaseModel):
    purchasing_dealer_id: Optional[int] = None
    fish_size: Optional[str] = None
    start_date: Optional[datetime] = None
    finish_date: Optional[datetime] = None
    amount_of_collection: Optional[int] = None
    purchasing_address: Optional[str] = None
    purchasing_address_level_1_id: Optional[int] = None
    purchasing_address_level_2_id: Optional[int] = None
    purchasing_address_level_3_id: Optional[int] = None

    class Config:
        orm_mode = True


class CollectSeasonCompleteUpdateRequest(BaseModel):
    purchasing_dealer_id: int
    fish_size: str 
    start_date: datetime
    finish_date: datetime 
    amount_of_collection: int 
    purchasing_address: str
    purchasing_address_level_1_id: int
    purchasing_address_level_2_id: int
    purchasing_address_level_3_id: int


    class Config:
        orm_mode = True


class CollectSeasonResponse(BaseModel):
    id: int = None
    base_season_pond_id: int = None
    purchasing_dealer_id: int = None
    fish_size: str = None
    start_date: datetime = None
    finish_date: datetime = None
    amount_of_collection: int = None
    purchasing_address: Optional[str] = None
    purchasing_address_level_1_id: Optional[int] = None
    purchasing_address_level_2_id: Optional[int] = None
    purchasing_address_level_3_id: Optional[int] = None
    purchasing_dealer: PurchasingDealersResponse = None
    purchasing_address_level_1: Optional[AddressLevel1Response] = None
    purchasing_address_level_2: Optional[AddressLevel2Response] = None
    purchasing_address_level_3: Optional[AddressLevel3Response] = None

    class Config:
        orm_mode = True

