from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.core.database import Base


class HarmfulAnimals(Base):
    __tablename__ = 'harmful_animals'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    images = relationship("Images", primaryjoin="and_(HarmfulAnimals.id==Images.record_id, "
                        "Images.record_type=='harmful_animals')", viewonly=True)
    deleted_at = Column(TIMESTAMP(timezone=True))
