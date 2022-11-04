from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.models.image import Images
from app.models.fish_type import FishTypes

from app.core.database import Base


class OriginalFishes(Base):
    __tablename__ = 'original_fishes'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    fish_type_id = Column(Integer, ForeignKey("fish_types.id"))
    fish_type = relationship("FishTypes", foreign_keys=[fish_type_id])
    images = relationship("Images", primaryjoin="and_(OriginalFishes.id==Images.record_id, "
                        "Images.record_type=='original_fishes')", viewonly=True)
    deleted_at = Column(TIMESTAMP(timezone=True))

