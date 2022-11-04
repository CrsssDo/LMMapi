from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.core.database import Base


class Units(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, nullable=False)
    unit_code = Column(String)
    code = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True))

