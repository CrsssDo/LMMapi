"""change type column estimated column to float

Revision ID: e98ff54cb44c
Revises: 6751d1b859e2
Create Date: 2022-07-28 16:04:47.692414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e98ff54cb44c'
down_revision = '6751d1b859e2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE dead_fish_diaries
    ALTER COLUMN mass TYPE float
    """)
    pass


def downgrade():
    pass
