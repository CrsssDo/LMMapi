"""create table food importation

Revision ID: 63b539504b87
Revises: 12b834d6adab
Create Date: 2022-05-23 10:39:07.512380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63b539504b87'
down_revision = '12b834d6adab'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'food_in',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('batch_code', sa.String, nullable=False),
        sa.Column('food_id', sa.Integer, nullable=False),
        sa.Column('adopt_area_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('inventory', sa.Integer, nullable=False),
        sa.Column('type_code', sa.String, nullable=False),
        sa.Column('in_date', sa.DATE, nullable=False),
        sa.Column('mfg_date', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('exp_date', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['food_id'], ['fish_foods.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['adopt_area_id'], ['adopt_areas.id'])

    )
    pass


def downgrade():
    op.drop_table('food_in')
    pass
