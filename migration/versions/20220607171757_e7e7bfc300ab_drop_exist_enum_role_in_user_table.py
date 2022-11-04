"""drop exist enum role in user table

Revision ID: e7e7bfc300ab
Revises: aae5cf7076ab
Create Date: 2022-06-07 17:17:57.908716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7e7bfc300ab'
down_revision = 'aae5cf7076ab'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE users DROP COLUMN role;
    """)
    pass


def downgrade():
    pass
