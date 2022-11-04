from typing import  List, Optional
from app.schemas.image import ImagesResponse

from pydantic import BaseModel, Field


class ShapeResponse(BaseModel):
    id: int
    code: str = None
    name: str = None
    images: List[ImagesResponse] = []


    class Config:
        orm_mode = True