from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.core.database import Base


class Chemistries(Base):
    __tablename__ = 'chemistries'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    receiver_code = Column(String)
    name = Column(String)
    uses = Column(String)
    element = Column(String)
    instructions_for_use = Column(String)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    chemistry_type_id = Column(Integer, ForeignKey("chemistry_types.id"))
    status = Column(Boolean, default=True)
    type = Column(String)
    analysed_date = Column(TIMESTAMP(timezone=True))
    declared_date = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True))
    supplier = relationship("Suppliers", foreign_keys=[supplier_id])
    chemistry_type = relationship("ChemistryTypes", foreign_keys=[chemistry_type_id])
    images = relationship("Images", primaryjoin="and_(Chemistries.id==Images.record_id, "
                        "Images.record_type=='chemistries')", viewonly=True)