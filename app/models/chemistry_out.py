from sqlalchemy import  Column, Integer, ForeignKey, String, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



from app.core.database import Base

class ChemistryOuts(Base):
    __tablename__ = 'chemistry_outs'
    id = Column(Integer, primary_key=True, nullable=False)
    chemistry_in_id = Column(Integer, ForeignKey("chemistry_ins.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)
    in_date = Column(DATE)
    pond_id = Column(Integer, ForeignKey("ponds.id"), nullable=False)
    note = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    pond = relationship("Ponds", foreign_keys=[pond_id])
    chemistry_in = relationship("ChemistryIns", back_populates="chemistry_outs")
