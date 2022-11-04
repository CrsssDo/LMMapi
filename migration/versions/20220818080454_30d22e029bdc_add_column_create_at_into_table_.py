"""add column create at into table specifications

Revision ID: 30d22e029bdc
Revises: 6d3df373cfcb
Create Date: 2022-08-18 08:04:54.459215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30d22e029bdc'
down_revision = '1c4888cf7154'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('specifications', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('specifications', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False))
    pass


def downgrade():
    pass
