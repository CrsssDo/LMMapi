from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.image import ImagesResponse
from app.schemas.fish_type import FishTypesResponse


class OriginalFishUpdateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    fish_type_id: int = None
    description: Optional[str] = None


class OriginFishCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    fish_type_id: int = None
    description: str = None

    class Config:
        orm_mode = True


class OriginFishResponse(BaseModel):
    id: int
    code: str = None
    name: str = None
    fish_type_id: int = None
    description: str = None
    deleted_at: datetime = None
    fish_type: FishTypesResponse = None


    class Config:
        orm_mode = True

class OriginFishDetailResponse(OriginFishResponse):
    images: List[ImagesResponse] = []
