from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.core.database import Base


class Environments(Base):
    __tablename__ = 'environments'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)