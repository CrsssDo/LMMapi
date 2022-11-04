from pydantic import BaseModel


class HistoryStatusResponse(BaseModel):
    id: int = None
    base_season_pond_id: int = None
    status: str = None

    class Config:
        orm_mode = True