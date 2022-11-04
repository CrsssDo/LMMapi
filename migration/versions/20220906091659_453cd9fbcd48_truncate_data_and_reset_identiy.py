"""truncate data and reset identiy

Revision ID: 453cd9fbcd48
Revises: 9929c36008d2
Create Date: 2022-09-06 09:16:59.562776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '453cd9fbcd48'
down_revision = '9929c36008d2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        TRUNCATE TABLE clean_seasons
        RESTART IDENTITY
    """)
    op.execute("""
        TRUNCATE TABLE collect_seasons
        RESTART IDENTITY
    """)
    op.execute("""
        TRUNCATE TABLE base_seasons
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE water_index_seasons
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE history_status_seasons
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE food_outs
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE food_ins
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE medicine_outs
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE medicine_ins
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE chemistry_outs
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE chemistry_ins
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE dead_fish_diaries
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE water_diaries_detail
        RESTART IDENTITY
    """)
    op.execute("""
        TRUNCATE TABLE water_diaries
        RESTART IDENTITY CASCADE
    """)
    op.drop_constraint('collect_seasons_base_season_id_fkey','collect_seasons')
    op.drop_constraint('clean_seasons_base_season_id_fkey','clean_seasons')
    op.drop_constraint('history_status_seasons_base_season_id_fkey','history_status_seasons')
    op.drop_constraint('water_index_seasons_base_season_id_fkey','water_index_seasons')
    pass


def downgrade():
    pass
