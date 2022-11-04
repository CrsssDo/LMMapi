"""create table dead fish diaries

Revision ID: ffc5d64af484
Revises: 26bd1992726f
Create Date: 2022-06-27 09:26:40.878033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffc5d64af484'
down_revision = '26bd1992726f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dead_fish_diaries',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('pond_id', sa.Integer, nullable=False),
        sa.Column('in_date', sa.DATE),
        sa.Column('quantity', sa.Integer),
        sa.Column('reason', sa.String),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False),
        sa.ForeignKeyConstraint(['pond_id'], ['ponds.id'])
    )
    pass


def downgrade():
    op.drop_table('dead_fish_diaries')
    pass
