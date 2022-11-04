from sqlalchemy import Column, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.measure_index import MeasureIndexes

from app.core.database import Base


class WaterDiariesDetail(Base):
    __tablename__ = "water_diaries_detail"
    id = Column(Integer, primary_key=True, nullable=False)
    water_diaries_id = Column(Integer, ForeignKey("water_diaries.id"), nullable=False)
    measure_index_id = Column(Integer, ForeignKey("measure_indexes.id"))
    status = Column(Boolean)
    water_measure_value = Column(Float)
    measure_index = relationship("MeasureIndexes", foreign_keys=[measure_index_id])
    water_diary = relationship("WaterDiaries", back_populates="water_diaries_value")

