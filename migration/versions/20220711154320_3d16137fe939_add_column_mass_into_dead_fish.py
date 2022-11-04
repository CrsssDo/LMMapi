"""add column mass into dead fish

Revision ID: 3d16137fe939
Revises: 12064a750355
Create Date: 2022-07-11 15:43:20.141100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d16137fe939'
down_revision = '12064a750355'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE dead_fish_diaries
    ADD COLUMN mass int
    """)
    pass


def downgrade():
    op.execute("""
    ALTER TABLE dead_fish_diaries
    DROP COLUMN mass
    """)
    pass
