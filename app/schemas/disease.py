from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from app.schemas.image import ImagesResponse

class DiseaseUpdateRequest(BaseModel):
    name: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = None


class DiseaseCreateRequest(BaseModel):
    name: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = None


class DiseaseResponse(BaseModel):
    id: int
    name: str = None
    code: str = None
    description: str = None
    deleted_at: datetime = None


    class Config:
        orm_mode = True

class DiseaseDetailResponse(DiseaseResponse):
    images: List[ImagesResponse] = []
