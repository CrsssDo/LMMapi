from sqlalchemy import Column, Integer, String, Float, ForeignKey, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text




from app.core.database import Base


class MedicineOut(Base):
    __tablename__ = 'medicine_outs'
    id = Column(Integer, primary_key=True, nullable=False)
    medicine_in_id = Column(Integer, ForeignKey("medicine_ins.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)
    in_date = Column(DATE)
    pond_id = Column(Integer, ForeignKey("ponds.id"), nullable=False)
    note = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    pond = relationship("Ponds", foreign_keys=[pond_id])

    medicine_in = relationship("MedicineIn", back_populates="medicine_outs")
