"""add column address lv2 and lv3 into table base season

Revision ID: 12064a750355
Revises: 661366e29b38
Create Date: 2022-07-08 15:47:59.694192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12064a750355'
down_revision = '661366e29b38'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    TRUNCATE base_seasons RESTART IDENTITY CASCADE;
    TRUNCATE collect_seasons RESTART IDENTITY CASCADE;
    TRUNCATE clean_seasons RESTART IDENTITY CASCADE;
    TRUNCATE water_index_seasons RESTART IDENTITY CASCADE;
    TRUNCATE history_status_seasons RESTART IDENTITY CASCADE;
    """)
    op.execute("""
    ALTER TABLE base_seasons
    ADD COLUMN supplier_address_level_2_id int,
    ADD COLUMN supplier_address_level_3_id int
    """)
    op.execute("""
    ALTER TABLE collect_seasons
    ADD COLUMN purchasing_address_level_2_id int,
    ADD COLUMN purchasing_address_level_3_id int
    """)
    pass


def downgrade():
    op.execute("""
    ALTER TABLE base_seasons
    DROP COLUMN supplier_address_level_2_id,
    DROP COLUMN supplier_address_level_3_id
    """)
    op.execute("""
    ALTER TABLE collect_seasons
    DROP COLUMN purchasing_address_level_2_id,
    DROP COLUMN purchasing_address_level_3_id
    """)
    pass
