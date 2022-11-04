from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.core.database import Base


class AddressLevel3(Base):
    __tablename__ = "address_level_3"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)


class AddressLevel2(Base):
    __tablename__ = "address_level_2"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    address_level_3_id = Column(Integer, ForeignKey("address_level_3.id"), nullable=False)
    address_level_3 = relationship("AddressLevel3", foreign_keys=[address_level_3_id])


class AddressLevel1(Base):
    __tablename__ = "address_level_1"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    address_level_2_id = Column(Integer, ForeignKey("address_level_2.id"), nullable=False)
    address_level_2 = relationship("AddressLevel2", foreign_keys=[address_level_2_id])
