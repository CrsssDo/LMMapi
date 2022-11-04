from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from app.models.user import User

from app.core.database import Base


class UserHistory(Base):
    __tablename__ = "user_histories"
    id = Column(Integer, primary_key=True, nullable=False)
    by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String)
    record_type = Column(String)
    record_id = Column(Integer)
    details = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    by_user = relationship(User, foreign_keys=[by_user_id])