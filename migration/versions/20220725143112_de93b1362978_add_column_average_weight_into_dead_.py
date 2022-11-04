"""add column average weight into dead fish diary

Revision ID: de93b1362978
Revises: 06963267fe8d
Create Date: 2022-07-25 14:31:12.140203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de93b1362978'
down_revision = '06963267fe8d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE dead_fish_diaries
    ADD COLUMN average_weight FLOAT,
    ADD COLUMN accumulated_loss INT,
    ADD COLUMN accumulated_exist INT,
    ADD COLUMN estimated_volume INT,
    ADD COLUMN health_condition VARCHAR
    """)
    op.execute("""
    ALTER TABLE dead_fish_diaries
    DROP COLUMN reason
    """)
    op.execute("""
        ALTER TABLE harmful_animals
        ADD COLUMN code VARCHAR
        """)
    op.execute("""
        ALTER TABLE diseases
        ADD COLUMN code VARCHAR
        """)
    pass


def downgrade():
    pass
