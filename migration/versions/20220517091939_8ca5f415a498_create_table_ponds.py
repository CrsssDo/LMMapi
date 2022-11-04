"""create table ponds

Revision ID: 8ca5f415a498
Revises: 9c41136a7ed2
Create Date: 2022-05-17 09:19:39.586310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ca5f415a498'
down_revision = '9c41136a7ed2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ponds',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String, nullable=False, unique=True),
        sa.Column('area', sa.Float, nullable=False),
        sa.Column('location', sa.String),
        sa.Column('adopt_area_id', sa.Integer, nullable=False),
        sa.Column('pond_type_id', sa.Integer, nullable=False),
        sa.Column('pond_categorize_id', sa.Integer, nullable=False),
        sa.Column('finished_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('status', sa.Boolean, default=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False),
        sa.ForeignKeyConstraint(['adopt_area_id'], ['adopt_areas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pond_type_id'], ['pond_types.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pond_categorize_id'], ['pond_categorizes.id'], ondelete='CASCADE')
    )
    pass


def downgrade():
    op.drop_table('ponds')
    pass
