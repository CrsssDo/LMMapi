"""create table medicines

Revision ID: 2ef7b8dce42f
Revises: fa52d6a7f5fc
Create Date: 2022-05-17 13:57:49.313055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ef7b8dce42f'
down_revision = 'fa52d6a7f5fc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'medicines',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String(255), nullable=False, unique=True),
        sa.Column('receiver_code', sa.String),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('uses', sa.String),
        sa.Column('element', sa.String),
        sa.Column('instructions_for_use', sa.String),
        sa.Column('status', sa.Boolean, default=True),
        sa.Column('supplier_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='SET NULL'),
        sa.Column('medicine_type', sa.String(255), nullable=False),
        sa.Column('analysed_date', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('declared_date', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('medicines')
    pass

