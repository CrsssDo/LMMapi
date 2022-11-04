from sqlalchemy import  Column, Integer, ForeignKey, String, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



from app.core.database import Base

class FoodOut(Base):
    __tablename__ = 'food_outs'
    id = Column(Integer, primary_key=True, nullable=False)
    food_in_id = Column(Integer, ForeignKey("food_ins.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)
    in_date = Column(DATE)
    pond_id = Column(Integer, ForeignKey("ponds.id"), nullable=False)
    note = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    pond = relationship("Ponds", foreign_keys=[pond_id])

    food_in = relationship("FoodIn", back_populates="food_outs")
