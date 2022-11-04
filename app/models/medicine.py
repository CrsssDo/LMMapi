from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.models.supplier import Suppliers
from app.models.medicine_type import MedicineTypes

from app.core.database import Base


class Medicines(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String(255), nullable=False)
    receiver_code = Column(String(255))
    name = Column(String(255), nullable=False)
    uses = Column(String)
    element = Column(String)
    instructions_for_use = Column(String)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    medicine_type_id = Column(Integer, ForeignKey("medicine_types.id"))
    status = Column(Boolean, default=True)
    medicine_type = Column(String)
    analysed_date = Column(TIMESTAMP(timezone=True))
    declared_date = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True))
    supplier = relationship("Suppliers", foreign_keys=[supplier_id])
    medicine_type = relationship("MedicineTypes", foreign_keys=[medicine_type_id])
    images = relationship("Images", primaryjoin="and_(Medicines.id==Images.record_id, "
                        "Images.record_type=='medicines')", viewonly=True)




