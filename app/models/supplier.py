from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.core.database import Base


class SupplierTypes(Base):
    __tablename__ = "supplier_types"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)


class Suppliers(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, nullable=False)
    supplier_code = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    address_level_1_id = Column(Integer, ForeignKey("address_level_1.id"), nullable=False)
    supplier_type_id = Column(Integer, ForeignKey("supplier_types.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True))
    address_level_1 = relationship("AddressLevel1", foreign_keys=[address_level_1_id])
    supplier_type = relationship("SupplierTypes", foreign_keys=[supplier_type_id])