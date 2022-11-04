"""create table adopt area adopt types

Revision ID: 9fc88042b270
Revises: e98ff54cb44c
Create Date: 2022-08-01 13:44:41.151304

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.adopt import AdoptAreas


# revision identifiers, used by Alembic.
revision = '9fc88042b270'
down_revision = 'e98ff54cb44c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'adopt_area_adopt_types',
        sa.Column('adopt_area_id', sa.Integer, primary_key=True),
        sa.Column('adopt_type_id', sa.Integer, primary_key=True),
        sa.ForeignKeyConstraint(['adopt_area_id'], ['adopt_areas.id']),
        sa.ForeignKeyConstraint(['adopt_type_id'], ['adopt_area_types.id'])
    )
    op.execute("""
        ALTER TABLE adopt_areas
        ALTER COLUMN adopt_area_type_id DROP NOT NULL
    """)
    pass


def downgrade():
    pass
