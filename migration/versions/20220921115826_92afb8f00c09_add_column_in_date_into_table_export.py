"""add column in date into table export

Revision ID: 92afb8f00c09
Revises: f675aa0d1f02
Create Date: 2022-09-21 11:58:26.270545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92afb8f00c09'
down_revision = 'f675aa0d1f02'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('food_outs', sa.Column('in_date', sa.DATE))
    op.add_column('medicine_outs', sa.Column('in_date', sa.DATE))
    op.add_column('chemistry_outs', sa.Column('in_date', sa.DATE))
    pass


def downgrade():
    pass
