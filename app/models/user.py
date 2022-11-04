from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import List
from app.models.user_images import UserImages
from app.models.adopt import AdoptAreas

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    code = Column(String(15), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(10), nullable=False)
    address = Column(String(50), nullable=False)
    active = Column(Boolean)
    unactivated_reason = Column(String)
    avatar_image_url = Column(String)
    before_identity_image_url = Column(String)
    after_identity_image_url = Column(String)
    address_level_1_id = Column(Integer, ForeignKey("address_level_1.id"), nullable=False)
    adopt_area_id = Column(Integer, ForeignKey("adopt_areas.id"), nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    adopt_area = relationship("AdoptAreas", foreign_keys=[adopt_area_id])
    address_level_1 = relationship("AddressLevel1", foreign_keys=[address_level_1_id])
    images = relationship("UserImages", primaryjoin="User.id==UserImages.user_id", viewonly=True)
    last_logged_in_date = Column(DateTime, nullable=False, server_default=text('now()'))

    