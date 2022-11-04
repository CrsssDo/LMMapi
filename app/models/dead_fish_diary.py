from sqlalchemy import  Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DATE
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.core.database import Base


class DeadFishDiaries(Base):
    __tablename__ = "dead_fish_diaries"
    id = Column(Integer, primary_key=True, nullable=False)
    pond_id = Column(Integer, ForeignKey("ponds.id"), nullable=False)
    in_date = Column(DATE, nullable=False)
    quantity = Column(Integer)
    mass = Column(Float)
    average_weight = Column(Float)
    accumulated_loss = Column(Integer)
    accumulated_exist = Column(Integer)
    estimated_volume = Column(Integer)
    health_condition = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    pond = relationship("Ponds", foreign_keys=[pond_id])
