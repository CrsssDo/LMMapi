"""create table measure indexes

Revision ID: 8720791a1220
Revises: 21010cefbc61
Create Date: 2022-06-16 16:54:29.163836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8720791a1220'
down_revision = '493eac03bf78'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'measure_indexes',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String(20), nullable=False),
        sa.Column('max_range', sa.Float),
        sa.Column('min_range', sa.Float),
        sa.Column('water_environment', sa.String(50), nullable=False),
        sa.Column('unit_id', sa.Integer),
        sa.ForeignKeyConstraint(['unit_id'], ['units.id'], ondelete='SET NULL'),
    )
    pass


def downgrade():
    op.drop_table(
        'measure_indexes'
    )
    pass

