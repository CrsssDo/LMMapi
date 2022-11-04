"""create table fish disease

Revision ID: f8d3d5dac848
Revises: 26ba26033da6
Create Date: 2022-05-17 15:56:30.362461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8d3d5dac848'
down_revision = '26ba26033da6'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'fish_diseases',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String)
    )
    pass


def downgrade():
    op.drop_table('fish_diseases')
    pass