"""add water environment into adopt area

Revision ID: 493eac03bf78
Revises: 90eb18eeab6b
Create Date: 2022-06-16 13:31:15.537961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '493eac03bf78'
down_revision = '90eb18eeab6b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE adopt_areas
    ADD COLUMN water_environment varchar(30) NOT NULL DEFAULT 'Nước ngọt'
    """)
    pass


def downgrade():
    op.drop_column(
        'adopt_areas',
        'water_environment'
    )
    pass
