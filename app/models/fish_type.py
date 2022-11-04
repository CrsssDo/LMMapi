from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.core.database import Base


class FishTypes(Base):
    __tablename__ = "fish_types"
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String)
    name = Column(String)
    deleted_at = Column(TIMESTAMP(timezone=True))
