from typing import List
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DATE
from app.models.pond import Ponds
from app.models.water_diary_detail import WaterDiariesDetail
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.core.database import Base


class WaterDiaries(Base):
    __tablename__ = "water_diaries"
    id = Column(Integer, primary_key=True, nullable=False)
    pond_id = Column(Integer, ForeignKey("ponds.id"), nullable=False)
    in_date = Column(DATE, nullable=False)
    comment = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    pond = relationship("Ponds", foreign_keys=[pond_id])
    water_diaries_value: List[WaterDiariesDetail] = relationship("WaterDiariesDetail", back_populates="water_diary")
    water_diary_histories = relationship("WaterDiaryHistories", back_populates="water_diary")
