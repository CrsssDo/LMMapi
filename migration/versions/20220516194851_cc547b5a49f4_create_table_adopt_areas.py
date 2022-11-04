"""create table adopt areas

Revision ID: cc547b5a49f4
Revises: c2a2da52d82b
Create Date: 2022-05-16 19:48:51.400711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc547b5a49f4'
down_revision = 'c2a2da52d82b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "adopt_areas",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("area_code", sa.String(255), nullable=False, unique=True),
        sa.Column("address", sa.String(255), nullable=False),
        sa.Column("area_owner", sa.String(255), nullable=False),
        sa.Column("address_level_1_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['address_level_1_id'], ['address_level_1.id'], ondelete='SET NULL'),
        sa.Column("adopt_area_type_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['adopt_area_type_id'], ['adopt_area_types.id'], ondelete='SET NULL'),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False)
    )
    pass


def downgrade():
    op.drop_table("adopt_areas")
    pass
