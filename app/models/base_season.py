from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship



from app.core.database import Base

class BaseSeasons(Base):
    __tablename__ = 'base_seasons'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String)
    status = Column(String)
    notes = Column(String)
    adopt_area_id = Column(Integer, ForeignKey("adopt_areas.id"))
    expected_start_date = Column(DATE)
    expected_end_date = Column(DATE)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    base_season_ponds = relationship("BaseSeasonPonds", primaryjoin="BaseSeasons.id==BaseSeasonPonds.base_season_id", order_by="BaseSeasonPonds.id")
    adopt_area = relationship("AdoptAreas", foreign_keys=[adopt_area_id])



