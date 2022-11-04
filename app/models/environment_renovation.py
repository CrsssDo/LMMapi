from sqlalchemy import DATE, Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.models.chemistry import Chemistries
from app.models.unit import Units

from app.core.database import Base


class EnvironmentRevovations(Base):
    __tablename__ = 'environment_renovations'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String)
    exp_date = Column(DATE)
    pond_id = Column(Integer)
    quantity = Column(Integer)
    unit_id = Column(Integer, ForeignKey("units.id"))
    chemistry_id = Column(Integer, ForeignKey("chemistries.id"), nullable=False)
    reason = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    unit = relationship("Units", foreign_keys=[unit_id])
    chemistry = relationship("Chemistries", foreign_keys=[chemistry_id])