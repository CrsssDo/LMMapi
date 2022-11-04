from datetime import datetime
from typing import List, Optional
from psycopg2 import Timestamp
from pydantic import BaseModel, Field
from app.schemas.image import ImagesResponse
from app.schemas.supplier import SupplierResponse
from app.schemas.food_type import FoodTypesResponse
from app.schemas.fish_type import FishTypesResponse


class FoodUpdateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    type: int = None
    receiver_code: Optional[str] = None
    name: str   
    uses: str
    food_type_id: int = None
    fish_type_id: int = None
    protein_value: int = None
    element: str
    instructions_for_use: Optional[str] = None
    supplier_id: int
    status: bool = True
    analysed_date: Optional[datetime] = None
    declared_date: Optional[datetime] = None


class FoodCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    type: int = None
    receiver_code: Optional[str] = None
    food_type_id: int = None
    fish_type_id: int = None
    protein_value: int = None
    name: str   
    uses: str
    element: str
    instructions_for_use: Optional[str] = None
    supplier_id: int
    status: bool = True
    analysed_date: Optional[datetime] = None
    declared_date: Optional[datetime] = None


class FoodResponse(BaseModel):
    id: int = None
    code: str = None
    name: str = None
    type: int = None
    receiver_code: str = None
    name: str = None
    uses: str = None
    element: str = None
    food_type_id: int = None
    fish_type_id: int = None
    protein_value: int = None
    instructions_for_use: str = None
    supplier_id: int = None
    status: bool = True
    analysed_date: datetime = None
    declared_date: datetime = None
    supplier: SupplierResponse = None
    deleted_at: datetime = None
    food_type: FoodTypesResponse = None
    fish_type: FishTypesResponse = None


    class Config:
        orm_mode = True

class FoodDetailResponse(FoodResponse):
    images: List[ImagesResponse] = []


class FoodStatusUpdateRequest(BaseModel):
    status: Optional[bool]

    class Config:
        orm_mode = True

