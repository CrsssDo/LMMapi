from fastapi import Query
from pydantic import BaseModel, Field

class FilterBase(BaseModel):
    limit: int = Query(default=10, lte=1000)
    offset: int = 0

class Capcha(BaseModel):
    token: str = Field(...)

    