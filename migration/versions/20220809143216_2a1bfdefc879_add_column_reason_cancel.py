"""add column reason cancel

Revision ID: 2a1bfdefc879
Revises: b5f58779a6fb
Create Date: 2022-08-09 14:32:16.143981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a1bfdefc879'
down_revision = 'b5f58779a6fb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('base_seasons', sa.Column('reason_cancel', sa.String()))
    pass


def downgrade():
    op.drop_column('base_seasons', 'reason_cancel')
    pass
