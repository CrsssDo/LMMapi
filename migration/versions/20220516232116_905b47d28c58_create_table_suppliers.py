"""create_table_suppliers

Revision ID: 905b47d28c58
Revises: 069865d2b185
Create Date: 2022-05-16 23:21:16.986141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '905b47d28c58'
down_revision = '069865d2b185'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('supplier_code', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('address', sa.String(255), nullable=False),
        sa.Column('address_level_1_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['address_level_1_id'], ['address_level_1.id'], ondelete='SET NULL'),
        sa.Column('supplier_type_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['supplier_type_id'], ['supplier_types.id'], ondelete='SET NULL'),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('suppliers')
    pass
