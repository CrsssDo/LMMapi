from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy.sql.expression import text
from app.models.unit import Units
from app.models.medicine_out import MedicineOut
from app.models.specification import Specifications


from app.core.database import Base


class MedicineIn(Base):
    __tablename__ = 'medicine_ins'
    id = Column(Integer, primary_key=True, nullable=False)
    batch_code = Column(String, nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    adopt_area_id = Column(Integer, ForeignKey("adopt_areas.id"), nullable=False)
    specification_id = Column(Integer, ForeignKey("specifications.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    quantity = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)
    in_date = Column(DATE, nullable=False)
    mfg_date = Column(TIMESTAMP(timezone=True), nullable=False)
    exp_date = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    medicine = relationship("Medicines", foreign_keys=[medicine_id])
    adopt_area = relationship("AdoptAreas", foreign_keys=[adopt_area_id])
    unit = relationship("Units", foreign_keys=[unit_id])
    specification = relationship("Specifications", foreign_keys=[specification_id])

    medicine_outs = relationship("MedicineOut", back_populates="medicine_in")

