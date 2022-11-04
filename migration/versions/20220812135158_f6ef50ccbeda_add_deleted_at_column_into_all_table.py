"""add deleted_at column into all table

Revision ID: f6ef50ccbeda
Revises: 259f06d8e730
Create Date: 2022-08-12 13:51:58.888353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6ef50ccbeda'
down_revision = '259f06d8e730'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('chemistries', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('diseases', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('equipments', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('medicines', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('foods', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('harmful_animals', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('original_fishes', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('measure_indexes', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('ponds', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('suppliers', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('purchasing_dealers', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.add_column('units', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    pass


def downgrade():
    pass
