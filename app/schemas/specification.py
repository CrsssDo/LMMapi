from datetime import datetime
from fastapi import Query, Form, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from app.schemas.image import ImagesResponse
from app.schemas.shape import ShapeResponse
from app.schemas.unit import UnitResponse
from app.core.schemal import FilterBase


class SpecificTypes(str, Enum):
    food = 'Thức ăn'
    medicine = 'Thuốc'
    chemistry = 'Hóa chất'


class SpecificationResponse(BaseModel):
    id: int
    code: str
    shape_id: int = None
    unit_id: int = None
    amount: int = None
    type: SpecificTypes = None
    created_at: datetime = None
    images: List[ImagesResponse] = []
    shape: ShapeResponse = None
    unit: UnitResponse = None


    class Config:
        orm_mode = True
        use_enum_values = True


class SpecificationCreateRequest(BaseModel):
    shape_id: int = None
    unit_id: int = None
    amount: int = None
    type: SpecificTypes = None

    class Config:
        orm_mode = True
        use_enum_values = True


class SpecificationCreateForm():
    def __init__(
        self,
        shape_id: int = Form(...),
        unit_id: int = Form(...),
        amount: int = Form(...),
        type: SpecificTypes = Form(...),
        image_data: UploadFile = File(...)
    ):
        self.shape_id = shape_id
        self.unit_id = unit_id
        self.amount = amount
        self.type = type
        self.image_data = image_data
    def dict(self):
        return self.__dict__  


class SpecificationFilter(FilterBase):
    code: str = Query(None)
    shape_id: int = Query(None)
    unit_id: int = Query(None)
    type: str = Query(None)

