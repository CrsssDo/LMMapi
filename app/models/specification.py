from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Specifications(Base):
    __tablename__ = 'specifications'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String)
    shape_id = Column(Integer, ForeignKey("shapes.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    amount = Column(Integer)
    type = Column(String)
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    shape = relationship("Shapes", foreign_keys=[shape_id])
    unit = relationship("Units", foreign_keys=[unit_id])
    images = relationship("Images", primaryjoin="and_(Specifications.id==Images.record_id, "
                        "Images.record_type=='specifications')", viewonly=True)
