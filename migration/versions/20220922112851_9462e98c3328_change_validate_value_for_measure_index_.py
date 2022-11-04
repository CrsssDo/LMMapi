"""change validate value for measure index code column

Revision ID: 9462e98c3328
Revises: 92afb8f00c09
Create Date: 2022-09-22 11:28:51.559002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9462e98c3328'
down_revision = '92afb8f00c09'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE measure_indexes ALTER COLUMN code TYPE varchar
    """)
    pass


def downgrade():
    pass
