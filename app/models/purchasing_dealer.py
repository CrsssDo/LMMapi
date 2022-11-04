from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.models.address import AddressLevel1

from app.core.database import Base


class PurchasingDealers(Base):
    __tablename__ = "purchasing_dealers"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    code = Column(String)
    address = Column(String)
    address_level_1_id = Column(Integer, ForeignKey("address_level_1.id"))
    address_level_1 = relationship("AddressLevel1", foreign_keys=[address_level_1_id])
    deleted_at = Column(TIMESTAMP(timezone=True))

