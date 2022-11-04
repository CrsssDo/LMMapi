from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy.sql.expression import text
from app.models.food_out import FoodOut



from app.core.database import Base


class FoodIn(Base):
    __tablename__ = 'food_ins'
    id = Column(Integer, primary_key=True, nullable=False)
    batch_code = Column(String, nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    adopt_area_id = Column(Integer, ForeignKey("adopt_areas.id"), nullable=False)
    specification_id = Column(Integer, ForeignKey("specifications.id"))
    quantity = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)
    type_code = Column(Integer, nullable=False)
    in_date = Column(DATE, nullable=False)
    mfg_date = Column(TIMESTAMP(timezone=True), nullable=False)
    exp_date = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    food = relationship("Foods", foreign_keys=[food_id])
    specification = relationship("Specifications", foreign_keys=[specification_id])
    adopt_area = relationship("AdoptAreas", foreign_keys=[adopt_area_id])
    food_outs = relationship("FoodOut", back_populates="food_in")
