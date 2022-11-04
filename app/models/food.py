from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.models.food_type import FoodTypes

from app.core.database import Base


class Foods(Base):
    __tablename__ = 'foods'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    type = Column(Integer)
    receiver_code = Column(String)
    name = Column(String)
    uses = Column(String)
    element = Column(String)
    instructions_for_use = Column(String)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    food_type_id = Column(Integer, ForeignKey("food_types.id"))
    fish_type_id = Column(Integer, ForeignKey("fish_types.id"))
    protein_value = Column(Integer)
    status = Column(Boolean, default=True)
    analysed_date = Column(TIMESTAMP(timezone=True))
    declared_date = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True))
    supplier = relationship("Suppliers", foreign_keys=[supplier_id])
    food_type = relationship("FoodTypes", foreign_keys=[food_type_id])
    fish_type = relationship("FishTypes", foreign_keys=[fish_type_id])
    images = relationship("Images", primaryjoin="and_(Foods.id==Images.record_id, "
                        "Images.record_type=='fish_foods')", viewonly=True)


