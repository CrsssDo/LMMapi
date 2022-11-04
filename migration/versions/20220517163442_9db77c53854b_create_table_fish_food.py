"""create table fish food

Revision ID: 9db77c53854b
Revises: f8d3d5dac848
Create Date: 2022-05-17 16:34:42.673451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9db77c53854b'
down_revision = 'f8d3d5dac848'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'fish_foods',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('type', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('fish_foods')
    pass
