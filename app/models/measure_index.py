from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.models.unit import Units

from app.core.database import Base


class MeasureIndexes(Base):
    __tablename__ = "measure_indexes"
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    max_range = Column(Float)
    min_range = Column(Float)
    water_environment = Column(String,nullable=False)
    status = Column(Boolean)
    unit_id = Column(Integer, ForeignKey("units.id") , nullable=False)
    unit = relationship("Units", foreign_keys=[unit_id])
    deleted_at = Column(TIMESTAMP(timezone=True))

