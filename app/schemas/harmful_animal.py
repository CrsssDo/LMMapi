from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.image import ImagesResponse


class HarmfulAnimalsResponse(BaseModel):
    id: int = None
    name: str = None
    code: str = None
    deleted_at: datetime = None


    class Config:
        orm_mode = True

class HarmfulAnimalDetailResponse(HarmfulAnimalsResponse):
    images: List[ImagesResponse] = []

class HarmfulAnimalCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

    class Config:
        orm_mode = True
