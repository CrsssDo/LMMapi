"""update code value some table

Revision ID: 6751d1b859e2
Revises: de93b1362978
Create Date: 2022-07-26 08:23:42.872702

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from app.models.fish_original import OriginalFishes
from app.models.supplier import Suppliers
from app.models.harmful_animal import HarmfulAnimals
from app.models.disease import Diseases
from app.models.pond import Ponds
from app.models.food_in import FoodIn
from app.models.medicine_in import MedicineIn
from app.models.chemistry_in import ChemistryIns
from app.core.database import get_db
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision = '6751d1b859e2'
down_revision = 'de93b1362978'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
