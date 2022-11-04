from sqlalchemy import Column, Float, Integer, ForeignKey, Boolean, Date, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.models.measure_index import MeasureIndexes

from app.core.database import Base


class WaterDiaryHistories(Base):
    __tablename__ = "water_diary_histories"
    id = Column(Integer, primary_key=True, nullable=False)
    water_diary_id = Column(Integer, ForeignKey("water_diaries.id"), nullable=False)
    measure_index_id = Column(Integer, ForeignKey("measure_indexes.id"))
    measure_value = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    measure_index = relationship("MeasureIndexes", foreign_keys=[measure_index_id])
    water_diary = relationship("WaterDiaries", back_populates="water_diary_histories")

