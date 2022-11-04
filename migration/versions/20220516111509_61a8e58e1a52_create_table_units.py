"""create table units

Revision ID: 61a8e58e1a52
Revises: 109281d6a2f5
Create Date: 2022-05-16 11:15:09.401737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61a8e58e1a52'
down_revision = '109281d6a2f5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "units",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("code", sa.Text, unique=True, nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), onupdate=sa.text('current_timestamp'),nullable=False)
    )
    pass


def downgrade():
    op.drop_table("units")
    pass
