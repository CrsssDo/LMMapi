from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy.sql.expression import text
from app.models.chemistry_out import ChemistryOuts
from app.models.specification import Specifications

from app.core.database import Base

class ChemistryIns(Base):
    __tablename__ = 'chemistry_ins'
    id = Column(Integer, primary_key=True, nullable=False)
    batch_code = Column(String, nullable=False)
    chemistry_id = Column(Integer, ForeignKey("chemistries.id"), nullable=False)
    adopt_area_id = Column(Integer, ForeignKey("adopt_areas.id"), nullable=False)
    specification_id = Column(Integer, ForeignKey("specifications.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    quantity = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)
    in_date = Column(DATE, nullable=False)
    mfg_date = Column(TIMESTAMP(timezone=True), nullable=False)
    exp_date = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    chemistry = relationship("Chemistries", foreign_keys=[chemistry_id])
    adopt_area = relationship("AdoptAreas", foreign_keys=[adopt_area_id])
    unit = relationship("Units", foreign_keys=[unit_id])
    specification = relationship("Specifications", foreign_keys=[specification_id])

    chemistry_outs = relationship("ChemistryOuts", back_populates="chemistry_in")
