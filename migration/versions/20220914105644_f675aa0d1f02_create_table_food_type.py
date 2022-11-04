"""create table food type

Revision ID: f675aa0d1f02
Revises: 0c3fea6a144d
Create Date: 2022-09-14 10:56:44.127121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f675aa0d1f02'
down_revision = '0c3fea6a144d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'fish_types',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String),
        sa.Column('name', sa.String),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True))
    )
    op.execute("""
        ALTER TABLE original_fishes
        ADD COLUMN fish_type_id int,
        ADD CONSTRAINT original_fishes_fish_type_id_fkey FOREIGN KEY(fish_type_id) REFERENCES fish_types(id)
    """)
    op.execute("""
        ALTER TABLE foods
        ADD COLUMN fish_type_id int,
        ADD CONSTRAINT foods_fish_type_id_fkey FOREIGN KEY(fish_type_id) REFERENCES fish_types(id)
    """)
    pass


def downgrade():
    pass
