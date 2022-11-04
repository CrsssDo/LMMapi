"""create table medicine out

Revision ID: 43b0e005b125
Revises: 93b9f645830b
Create Date: 2022-05-24 14:29:18.842421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43b0e005b125'
down_revision = '93b9f645830b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'medicine_out',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('medicine_in_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Float, nullable=False),
        sa.Column('inventory', sa.Integer, nullable=False),
        sa.Column('pond_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['medicine_in_id'], ['medicine_in.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pond_id'], ['ponds.id'], ondelete='SET NULL'),
    )
    pass


def downgrade():
    op.drop_table('medicine_out')
    pass


