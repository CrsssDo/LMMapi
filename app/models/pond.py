from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.models.dead_fish_diary import DeadFishDiaries
from app.models.adopt import AdoptAreas

from app.core.database import Base


class PondTypes(Base):
    __tablename__ = 'pond_types'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String)
    name = Column(String, nullable=False)
    symbol = Column(String)
    deleted_at = Column(TIMESTAMP(timezone=True))


class PondCategorizes(Base):
    __tablename__ = 'pond_categorizes'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


class Ponds(Base):
    __tablename__ = 'ponds'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    area = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    location = Column(String)
    pond_map_name = Column(String)
    adopt_area_id = Column(Integer, ForeignKey("adopt_areas.id", ondelete="CASCADE"), nullable=False)
    pond_type_id = Column(Integer, ForeignKey("pond_types.id", ondelete="CASCADE"), nullable=False)
    pond_categorize_id = Column(Integer, ForeignKey("pond_categorizes.id", ondelete="CASCADE"), nullable=False)
    finished_date = Column(TIMESTAMP(timezone=True))
    number_order = Column(Integer)
    status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True))
    adopt_area = relationship("AdoptAreas", foreign_keys=[adopt_area_id])
    pond_type = relationship("PondTypes", foreign_keys=[pond_type_id])
    pond_categorize = relationship("PondCategorizes", foreign_keys=[pond_categorize_id])
    dead_fish = relationship("DeadFishDiaries", primaryjoin="and_(Ponds.id==DeadFishDiaries.pond_id, "
                        f"DeadFishDiaries.in_date=='{datetime.now().date()}')", viewonly=True)
    images = relationship("Images", primaryjoin="and_(Ponds.id==Images.record_id, "
                        "Images.record_type=='ponds')", viewonly=True)




