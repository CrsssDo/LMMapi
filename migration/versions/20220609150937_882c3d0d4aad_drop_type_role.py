"""drop type role

Revision ID: 882c3d0d4aad
Revises: e7e7bfc300ab
Create Date: 2022-06-09 15:09:37.758737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '882c3d0d4aad'
down_revision = 'e7e7bfc300ab'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        DROP TYPE roles;
        """)
    pass


def downgrade():
    pass
