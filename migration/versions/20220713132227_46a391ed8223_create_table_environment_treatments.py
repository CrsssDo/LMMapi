"""create table environment treatments

Revision ID: 46a391ed8223
Revises: e5c3ad9eddac
Create Date: 2022-07-13 13:22:27.389294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46a391ed8223'
down_revision = 'e5c3ad9eddac'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'environment_renovations',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String),
        sa.Column('exp_date', sa.DATE),
        sa.Column('pond_id', sa.Integer),
        sa.Column('quantity', sa.Integer),
        sa.Column('chemistry_id', sa.Integer),
        sa.Column('unit_id', sa.Integer),
        sa.Column('reason', sa.String),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False),
        sa.ForeignKeyConstraint(['chemistry_id'], ['chemistries.id']),
        sa.ForeignKeyConstraint(['pond_id'], ['ponds.id']),
        sa.ForeignKeyConstraint(['unit_id'], ['units.id'])
    )
    pass


def downgrade():
    op.drop_table('environment_renovations')
    pass
