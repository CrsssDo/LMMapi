"""add column activate and unactivate reason into user

Revision ID: c8069d4be0d0
Revises: 2a1bfdefc879
Create Date: 2022-08-10 08:43:41.787331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8069d4be0d0'
down_revision = '2a1bfdefc879'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        ALTER TABLE users
        ADD COLUMN active bool default true
    """)
    op.execute("""
        ALTER TABLE users
        ADD COLUMN unactivated_reason varchar
    """)   
    pass



def downgrade():
    op.drop_column('users','active')
    op.drop_column('users','unactivated_reason')
    pass
