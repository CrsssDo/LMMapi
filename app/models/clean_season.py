from sqlalchemy import DATETIME, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


from app.core.database import Base

class CleanSeasons(Base):
    __tablename__ = 'clean_seasons'
    id = Column(Integer, primary_key=True, nullable=False)
    base_season_pond_id = Column(Integer, ForeignKey("base_season_ponds.id"))
    start_date = Column(DATETIME)
    finish_date = Column(DATETIME)
    process_description = Column(String)
    time_clear_pond = Column(String)
    time_between_season = Column(String)
    chemical_used = Column(String)
