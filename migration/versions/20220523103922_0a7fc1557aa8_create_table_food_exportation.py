"""create table food exportation

Revision ID: 0a7fc1557aa8
Revises: 63b539504b87
Create Date: 2022-05-23 10:39:22.925324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a7fc1557aa8'
down_revision = '63b539504b87'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'food_out',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('food_in_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('inventory', sa.Integer, nullable=False),
        sa.Column('pond_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['food_in_id'], ['food_in.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pond_id'], ['ponds.id'], ondelete='SET NULL'),
    )
    pass


def downgrade():
    op.drop_table('food_out')
    pass
