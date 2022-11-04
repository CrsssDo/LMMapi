from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.models.equipment import Equipments
from app.models.medicine import Medicines
from app.models.chemistry import Chemistries
from app.models.harmful_animal import HarmfulAnimals
from app.models.food import Foods
from app.models.disease import Diseases
from app.models.pond import Ponds
from app.models.shape import Shapes
from app.models.specification import Specifications

from app.core.database import Base

class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    ext = Column(String(55), nullable=False)
    url = Column(String, nullable=False)
    record_id = Column(Integer,
                ForeignKey("specifications.id"),
                ForeignKey("shapes.id"),
                ForeignKey("ponds.id"), 
                ForeignKey("diseases.id"),
                ForeignKey("medicines.id"),
                ForeignKey("original_fishes.id"),
                ForeignKey("foods.id"),
                ForeignKey("equipments.id"),
                ForeignKey("harmful_animals.id"),
                ForeignKey("chemistries.id"),
                nullable=False)
    record_type = Column(String, nullable=False)
    sub_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)



