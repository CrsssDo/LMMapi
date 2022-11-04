from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.core.database import Base


class FoodTypes(Base):
    __tablename__ = "food_types"
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String)
    name = Column(String)
    deleted_at = Column(TIMESTAMP(timezone=True))
