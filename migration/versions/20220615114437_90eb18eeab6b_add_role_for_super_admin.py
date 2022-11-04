"""add role for super admin

Revision ID: 90eb18eeab6b
Revises: 85c763f16200
Create Date: 2022-06-15 11:44:37.019586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90eb18eeab6b'
down_revision = '85c763f16200'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    UPDATE users
    SET role = 'Super Admin'
    WHERE id = 1
    """)
    pass


def downgrade():
    pass
