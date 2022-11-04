from enum import Enum
from typing import List, Optional
from app.schemas.address import AddressLevel1Response

from pydantic import BaseModel, Field


class AdoptAreaWaterEnviroment(str, Enum):
    fresh_water = 'Nước ngọt'
    salt_wate = 'Nước mặn'


class AdoptsTypeResponse(BaseModel):
    id: int = Field(alias='adopt_type_id')
    name: str = Field(alias='type_name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class AdoptUpdateRequest(BaseModel):
    area_owner: str = Field(..., min_length=2, max_length=100)
    address: Optional[str] = None
    water_environment: AdoptAreaWaterEnviroment = None
    address_level_1_id: int = None
    adopt_types: List[int] = []


    class Config:
        use_enum_values = True



class AdoptCreateRequest(BaseModel):
    area_owner: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=2, max_length=100)
    water_environment: AdoptAreaWaterEnviroment = None
    address_level_1_id: int = None
    adopt_types: List[int] = []

    class Config:
        orm_mode = True
        use_enum_values = True


class AdoptResponse(BaseModel):
    id: int
    area_code: Optional[str] = None
    address: Optional[str] = None
    area_owner: Optional[str] = None
    water_environment: str = None
    address_level_1_id: int = None
    adopt_area_type_id: int = None
    adopt_types: List[AdoptsTypeResponse] = []
    address_level_1: AddressLevel1Response = None

    class Config:
        orm_mode = True

