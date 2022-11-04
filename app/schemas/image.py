from typing import  Optional
from enum import Enum

from pydantic import BaseModel, Field


class ImagesType(str, Enum):
    pond_types = 'ponds'
    medicine_types = 'medicines'
    adopt_area_types = 'adopt_areas'
    equipment_types = 'equipments'
    fish_disease_types = 'fish_diseases'
    fish_food_types = 'fish_foods'
    original_fish_types = 'original_fishes'
    harmful_animal_types = 'harmful_animals'
    chemistry_types = 'chemistries'
    shape_types = 'shapes'
    specification_types = 'specifications'


class MedicineImageSubType(str, Enum):
    medicine_image_subtypes = 'medicine_image'
    medicine_certificate_subtypes = 'medicine_certificate_image'

class ChemistryImageSubType(str, Enum):
    chemistry_image_subtypes = 'chemistry_image'
    chemistry_certificate_subtypes = 'chemistry_certificate_image'

class FoodImageSubType(str, Enum):
    food_image_subtypes = 'food_image'
    food_certificate_subtypes = 'food_certificate_image'

class ImagesResponse(BaseModel):
    id: int
    record_id: int = None
    file_name: str = None
    record_type: str = None
    sub_type: str = None
    url: str = None

    class Config:
        orm_mode = True
