from typing import Optional

from pydantic import BaseModel


class AddressLevel3Response(BaseModel):
    id: int
    name: Optional[str] = None

    class Config:
        orm_mode = True

class AddressLevel2Response(BaseModel):
    id: int
    name: Optional[str] = None
    address_level_3: AddressLevel3Response = None

    class Config:
        orm_mode = True

class AddressLevel1Response(BaseModel):
    id: int
    name: Optional[str] = None
    address_level_2: AddressLevel2Response = None

    class Config:
        orm_mode = True
