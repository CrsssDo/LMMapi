from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.image import ImagesResponse


class EquipmentUpdateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None


class EquipmentCreateRequest(BaseModel):
    code: Optional[str] = None
    name: str = Field(..., min_length=2, max_length=255)
    description: str = None

    class Config:
        orm_mode = True


class EquipmentResponse(BaseModel):
    id: int
    code: str = None
    name: str = None
    description: str = None
    deleted_at: datetime = None


    class Config:
        orm_mode = True

class EquipmentDetailResponse(EquipmentResponse):
    images: List[ImagesResponse] = []

