from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship



from app.core.database import Base

class HistoryStatusSeasons(Base):
    __tablename__ = 'history_status_seasons'
    id = Column(Integer, primary_key=True, nullable=False)
    base_season_pond_id = Column(Integer, ForeignKey("base_season_ponds.id"))
    status = Column(String)
    