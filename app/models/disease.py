from typing import List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP


from app.core.database import Base


class Diseases(Base):
    __tablename__ = 'diseases'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String)
    description = Column(String)
    images = relationship("Images", primaryjoin="and_(Diseases.id==Images.record_id, "
                        "Images.record_type=='fish_diseases')", viewonly=True)
    deleted_at = Column(TIMESTAMP(timezone=True))




