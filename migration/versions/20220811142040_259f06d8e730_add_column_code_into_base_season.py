"""add column code into base season

Revision ID: 259f06d8e730
Revises: c8069d4be0d0
Create Date: 2022-08-11 14:20:40.317136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '259f06d8e730'
down_revision = 'c8069d4be0d0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('base_seasons', sa.Column('code', sa.String()))
    op.execute(f"""
        UPDATE base_seasons as b
        SET code =  CONCAT('VNC-','000', b.id)
        WHERE id < 10
    """)
    op.execute(f"""
        UPDATE base_seasons as b
        SET code =  CONCAT('VNC-','00', b.id)
        WHERE id < 100 and id >= 10
    """)
    op.execute(f"""
        UPDATE base_seasons as b
        SET code =  CONCAT('VNC-','0', b.id)
        WHERE id < 1000 and id >= 100
    """)
    pass


def downgrade():
    op.drop_column('base_seasons', 'code')
    pass
