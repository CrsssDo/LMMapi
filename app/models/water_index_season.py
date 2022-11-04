from typing import List
from sqlalchemy import Column, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.measure_index import MeasureIndexes

from app.core.database import Base


class WaterIndexSeasons(Base):
    __tablename__ = "water_index_seasons"
    id = Column(Integer, primary_key=True, nullable=False)
    base_season_pond_id = Column(Integer, ForeignKey("base_season_ponds.id"))
    measure_index_id = Column(Integer, ForeignKey("measure_indexes.id"))
    status = Column(Boolean)
    water_measure_value = Column(Float)
    measure_indexes = relationship("MeasureIndexes", foreign_keys=[measure_index_id])

