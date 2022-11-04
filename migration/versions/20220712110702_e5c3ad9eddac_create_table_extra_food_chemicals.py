"""create table extra food chemicals

Revision ID: e5c3ad9eddac
Revises: 12064a750355
Create Date: 2022-07-12 11:07:02.696046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c3ad9eddac'
down_revision = '3d16137fe939'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chemistries',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String, nullable=False),
        sa.Column('receiver_code', sa.String),
        sa.Column('name', sa.String),
        sa.Column('uses', sa.String),
        sa.Column('element', sa.String),
        sa.Column('instructions_for_use', sa.String),
        sa.Column('status', sa.Boolean, default=True),
        sa.Column('supplier_id', sa.Integer),
        sa.Column('type', sa.String),
        sa.Column('analysed_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('declared_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'])
    )
    pass


def downgrade():
    op.drop_table('chemistries')
    pass
