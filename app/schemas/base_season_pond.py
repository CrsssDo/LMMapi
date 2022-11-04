from enum import Enum
from typing import List, Optional
from datetime import date, datetime
from app.schemas.pond import PondsResponse
from app.schemas.supplier import SupplierResponse
from app.schemas.fish_original import OriginFishResponse
from app.schemas.address import AddressLevel1Response, AddressLevel2Response, AddressLevel3Response
from app.schemas.purchasing_dealer import PurchasingDealersResponse
from app.schemas.collect_season import CollectSeasonResponse
from app.schemas.clean_season import CleanSeasonResponse
from app.schemas.water_index_season import WaterIndexValueResponse
from app.schemas.history_status_season import HistoryStatusResponse

from pydantic import BaseModel, Field

class BaseSeasonPondsStatus(str, Enum):
    waiting = 'Chờ nuôi'
    cancel = 'Đã hủy'
    activating = 'Đang nuôi'
    collecting = 'Đang thu hoạch'
    collected = 'Đã thu hoạch'
    cleaning = 'Đang vệ sinh'
    cleaned = 'Đã vệ sinh'
    checking = 'Đang kiểm tra'
    checked = 'Đã kiểm tra'
    finished = 'Kết thúc'


class BaseSeasonPondCreateRequest(BaseModel):
    pond_id: int = None
    origin_fish_id: int = None
    status: BaseSeasonPondsStatus = None

    class Config:
        orm_mode = True
        use_enum_values = True

class BaseSeasonValue(BaseModel):
    water_index: List[WaterIndexValueResponse] = []


class BaseSeasonPondResponse(BaseModel):
    id: int
    code: str = None
    pond_id: int = None
    origin_fish_id: int = None
    supplier_id: int = None
    status: str = None
    in_date: date = None
    quantity: int = None
    density: str = None
    amount_of_quantity: int = None
    reason_cancel: str = None
    water_index_poison: str = None
    note: str = None
    comment: str = None
    created_at: datetime
    updated_at: datetime
    supplier_address: str = None
    supplier_address_level_1_id: int = None
    supplier_address_level_2_id: int = None
    supplier_address_level_3_id: int = None
    origin_fish: OriginFishResponse = None
    supplier: SupplierResponse = None
    supplier_address_level_1: AddressLevel1Response = None
    supplier_address_level_2: AddressLevel2Response = None
    supplier_address_level_3: AddressLevel3Response = None
    pond: PondsResponse = None
    collect: CollectSeasonResponse = None
    clean: CleanSeasonResponse = None
    water_indexes: List[WaterIndexValueResponse] = None
    status_histories: List[HistoryStatusResponse] = []


    class Config:
        orm_mode = True


class BaseSeasonPondsUpdateRequest(BaseModel):
    origin_fish_id: Optional[int] = None
    supplier_id: Optional[int] = None
    in_date: Optional[date] = None
    quantity: Optional[int] = None
    density: Optional[str] = None
    amount_of_quantity: Optional[int] = None
    supplier_address: Optional[str] = None
    supplier_address_level_1_id: Optional[int] = None
    supplier_address_level_2_id: Optional[int] = None
    supplier_address_level_3_id: Optional[int] = None
    reason_cancel: Optional[str] = None
    note: Optional[str] = None
    comment: Optional[str] = None

    class Config:
        orm_mode = True

class BaseSeasonsCompleteUpdateRequest(BaseModel):
    origin_fish_id: int
    supplier_id: int 
    in_date: date
    quantity: int 
    density: str
    amount_of_quantity: int
    supplier_address: str
    supplier_address_level_1_id: int
    supplier_address_level_2_id: int = None
    supplier_address_level_3_id: int = None
    reason_cancel: Optional[str] = None
    note: str
    comment: Optional[str] = None

    class Config:
        orm_mode = True

class BaseSeasonUpdateStatusRequest(BaseModel):
    status: BaseSeasonPondsStatus = None

    class Config:
        orm_mode = True
        use_enum_values = True


