from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.database import Base


class Equipments(Base):
    __tablename__ = 'equipments'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    images = relationship("Images", primaryjoin="and_(Equipments.id==Images.record_id, "
                        "Images.record_type=='equipments')", viewonly=True)
    deleted_at = Column(TIMESTAMP(timezone=True))

