from typing import Optional

from pydantic import BaseModel


class EnvironmentsResponse(BaseModel):
    id: int
    code: str
    name: str = None
    description: str = None

    class Config:
        orm_mode = True
