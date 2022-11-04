"""add users logged date

Revision ID: b5f58779a6fb
Revises: 9fc88042b270
Create Date: 2022-08-09 10:57:52.418146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5f58779a6fb'
down_revision = '9fc88042b270'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', 
        sa.Column('last_logged_in_date', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_column('users', 'last_logged_in_date')
