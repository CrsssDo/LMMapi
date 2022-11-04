"""create table water diaries

Revision ID: 26bd1992726f
Revises: e2d8afa1010c
Create Date: 2022-06-20 10:17:21.533674

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26bd1992726f'
down_revision = 'e2d8afa1010c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'water_diaries',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('pond_id', sa.Integer, nullable=False),
        sa.Column('in_date', sa.DATE),
        sa.Column('comment', sa.String),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False),
        sa.ForeignKeyConstraint(['pond_id'], ['ponds.id'])
    )
    op.create_table(
        'water_diaries_detail',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('water_diaries_id', sa.Integer, nullable=False),
        sa.Column('measure_index_id', sa.Integer),
        sa.Column('water_measure_value', sa.Float),
        sa.ForeignKeyConstraint(['water_diaries_id'], ['water_diaries.id']),
        sa.ForeignKeyConstraint(['measure_index_id'], ['measure_indexes.id'])
    )
    pass


def downgrade():
    op.drop_table('water_diaries_detail')
    op.drop_table('water_diaries')
    pass

