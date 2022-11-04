from unicodedata import name
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.core.database import Base


class Shapes(Base):
    __tablename__ = "shapes"
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String)
    name = Column(String)
    deleted_at = Column(TIMESTAMP(timezone=True))
    images = relationship("Images", primaryjoin="and_(Shapes.id==Images.record_id, "
                        "Images.record_type=='shapes')", viewonly=True)

