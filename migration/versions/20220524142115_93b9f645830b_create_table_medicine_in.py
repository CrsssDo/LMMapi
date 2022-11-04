"""create table medicine in

Revision ID: 93b9f645830b
Revises: 0a7fc1557aa8
Create Date: 2022-05-24 14:21:15.263458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93b9f645830b'
down_revision = '0a7fc1557aa8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'medicine_in',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('batch_code', sa.String, nullable=False),
        sa.Column('medicine_id', sa.Integer, nullable=False),
        sa.Column('adopt_area_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('inventory', sa.Integer, nullable=False),
        sa.Column('type_code', sa.String, nullable=False),
        sa.Column('in_date', sa.DATE, nullable=False),
        sa.Column('mfg_date', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('exp_date', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['medicine_id'], ['medicines.id'], ondelete='SET NULL'),
    )
    pass


def downgrade():
    op.drop_table('medicine_in')
    pass
