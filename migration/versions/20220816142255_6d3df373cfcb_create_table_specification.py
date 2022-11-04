"""create table specification

Revision ID: 6d3df373cfcb
Revises: f6ef50ccbeda
Create Date: 2022-08-16 14:22:55.991974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d3df373cfcb'
down_revision = 'e761744481a7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'specifications',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String),
        sa.Column('shape_id', sa.Integer),
        sa.Column('unit_id', sa.Integer),
        sa.Column('amount', sa.Integer),
        sa.Column('type', sa.String),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)),
        sa.ForeignKeyConstraint(['shape_id'], ['shapes.id']),
        sa.ForeignKeyConstraint(['unit_id'], ['units.id'])
    )
    
    pass


def downgrade():
    # op.drop_table('specifications')
    pass
