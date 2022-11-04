"""change type food_in column

Revision ID: 06963267fe8d
Revises: 4379080f99e8
Create Date: 2022-07-22 08:40:15.440718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06963267fe8d'
down_revision = '4379080f99e8'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    UPDATE food_ins
    SET type_code = 0
    """)
    op.execute("""
    ALTER TABLE food_ins
    ALTER COLUMN type_code TYPE int
    USING type_code::integer
    """)
    op.execute("""
    ALTER TABLE medicine_ins
    DROP COLUMN type_code,
    ADD COLUMN unit_id int
    """)
    op.execute("""
    ALTER TABLE chemistry_ins
    DROP COLUMN type_code,
    ADD COLUMN unit_id int
    """)
    op.create_foreign_key(
        "medicine_ins_unit_id_fkey", "medicine_ins",
        "units", ["unit_id"] , ["id"]
    )
    op.create_foreign_key(
        "chemistry_ins_unit_id_fkey", "chemistry_ins",
        "units", ["unit_id"] , ["id"]
    )
    pass


def downgrade():
    pass
