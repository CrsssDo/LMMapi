from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.models.address import AddressLevel1
from sqlalchemy.ext.associationproxy import association_proxy


from app.core.database import Base


class AdoptAreaAdoptTypes(Base):
    __tablename__ = "adopt_area_adopt_types"
    adopt_area_id = Column(ForeignKey('adopt_areas.id'), primary_key=True)
    adopt_type_id = Column(ForeignKey('adopt_area_types.id'), primary_key=True)
    adopt_area = relationship("AdoptAreas", back_populates="adopt_types")
    adopt_type = relationship("AdoptAreaTypes", back_populates="adopt_areas")

    type_name = association_proxy(target_collection='adopt_type', attr='name')


class AdoptAreaTypes(Base):
    __tablename__ = "adopt_area_types"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    adopt_areas = relationship("AdoptAreaAdoptTypes", back_populates='adopt_type')



class AdoptAreas(Base):
    __tablename__ = "adopt_areas"
    id = Column(Integer, primary_key=True, nullable=False)
    area_code = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    area_owner = Column(String, nullable=False)
    water_environment = Column(String(30), nullable=False)
    address_level_1_id = Column(Integer, ForeignKey("address_level_1.id"), nullable=False)
    adopt_area_type_id = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    address_level_1 = relationship("AddressLevel1", foreign_keys=[address_level_1_id])
    adopt_types = relationship("AdoptAreaAdoptTypes", back_populates='adopt_area')
    


