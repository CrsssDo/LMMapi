from datetime import datetime
from typing import  Optional

from pydantic import BaseModel, Field


class ChemistryTypesResponse(BaseModel):
    id: int
    code: str = None
    name: str = None
    deleted_at: datetime = None

    class Config:
        orm_mode = True