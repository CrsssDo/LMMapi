"""add default value into table adopt area

Revision ID: e356f5dbb3df
Revises: 51da280910aa
Create Date: 2022-10-11 15:17:59.131108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e356f5dbb3df'
down_revision = '51da280910aa'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    INSERT INTO adopt_areas(area_code, address, area_owner, water_environment, address_level_1_id, adopt_area_type_id)
    VALUES ('AR001','11/2 An Xuan', 'Hao', 'Nước mặn', 1, 1)
    """)
    op.execute("""
    INSERT INTO adopt_area_adopt_types(adopt_area_id, adopt_type_id)
    VALUES (1, 2), (1, 1)

    """)
    pass


def downgrade():
    pass
