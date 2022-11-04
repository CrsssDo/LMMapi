"""create table fish original

Revision ID: cfed8e8b9aef
Revises: ac59f176b19e
Create Date: 2022-05-18 08:51:57.811083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfed8e8b9aef'
down_revision = 'ac59f176b19e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'original_fishes',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
    )
    pass


def downgrade():
    op.drop_table('original_fishes')
    pass

