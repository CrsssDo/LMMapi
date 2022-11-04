"""add column pond map name into pond

Revision ID: 9929c36008d2
Revises: e846e3a5992b
Create Date: 2022-08-31 15:49:46.302148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9929c36008d2'
down_revision = 'e846e3a5992b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ponds', sa.Column('pond_map_name', sa.String))
    pass


def downgrade():
    op.drop_column('ponds', 'pond_map_name')
    pass
