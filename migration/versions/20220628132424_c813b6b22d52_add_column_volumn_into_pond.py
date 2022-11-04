"""add column volumn into pond

Revision ID: c813b6b22d52
Revises: ffc5d64af484
Create Date: 2022-06-28 13:24:24.381248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c813b6b22d52'
down_revision = 'ffc5d64af484'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE ponds
    ALTER COLUMN area TYPE int,
    ADD COLUMN volume int
    """)
    pass


def downgrade():
    op.execute("""
    ALTER TABLE ponds
    DROP COLUMN int
    """)
    pass
