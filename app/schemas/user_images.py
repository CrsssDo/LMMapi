from typing import  Optional

from pydantic import BaseModel, Field


class UserImagesResponse(BaseModel):
    id: int
    user_id: int
    other_image_url: str = None

    class Config:
        orm_mode = True