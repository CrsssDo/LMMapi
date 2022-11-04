"""create_table_equipment

Revision ID: ac59f176b19e
Revises: 9db77c53854b
Create Date: 2022-05-17 20:37:14.988701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac59f176b19e'
down_revision = '9db77c53854b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'equipments',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
    )
    pass


def downgrade():
    op.drop_table('equipments')
    pass

