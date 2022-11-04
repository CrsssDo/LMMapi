"""drop and add another constranint

Revision ID: 35a9aae87f8b
Revises: 1c20c7b66ce1
Create Date: 2022-06-06 08:24:57.509950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35a9aae87f8b'
down_revision = '1c20c7b66ce1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE medicine_outs
    ALTER COLUMN quantity TYPE int
    """)

    op.drop_constraint(
        table_name='food_ins',
        constraint_name='food_in_food_id_fkey'
    )

    op.drop_constraint(
        table_name='food_ins',
        constraint_name='food_in_adopt_area_id_fkey'
    )

    op.create_foreign_key(
        "food_ins_food_id_fkey", "food_ins",
        "foods", ["food_id"] , ["id"]
    )

    op.create_foreign_key(
        "food_ins_adopt_area_id_fkey", "food_ins",
        "adopt_areas", ["adopt_area_id"] , ["id"]
    )

    op.drop_constraint(
        table_name='food_outs',
        constraint_name='food_out_pond_id_fkey'
    )

    op.drop_constraint(
        table_name='food_outs',
        constraint_name='food_out_food_in_id_fkey'
    )

    op.create_foreign_key(
        "food_outs_food_in_id_fkey", "food_outs",
        "food_ins", ["food_in_id"] , ["id"]
    )

    op.create_foreign_key(
        "food_outs_pond_id_fkey", "food_outs",
        "ponds", ["pond_id"] , ["id"]
    )

    op.drop_constraint(
        table_name='medicine_ins',
        constraint_name='medicine_in_medicine_id_fkey'
    )

    op.create_foreign_key(
        "medicine_ins_food_id_fkey", "medicine_ins",
        "medicines", ["medicine_id"] , ["id"]
    )

    op.create_foreign_key(
        "medicine_ins_adopt_area_id_fkey", "medicine_ins",
        "adopt_areas", ["adopt_area_id"] , ["id"]
    )

    op.drop_constraint(
        table_name='medicine_outs',
        constraint_name='medicine_out_pond_id_fkey'
    )

    op.drop_constraint(
        table_name='medicine_outs',
        constraint_name='medicine_out_medicine_in_id_fkey'
    )

    op.create_foreign_key(
        "medicine_outs_medicine_in_id_fkey", "medicine_outs",
        "medicine_ins", ["medicine_in_id"] , ["id"]
    )

    op.create_foreign_key(
        "medicine_outs_pond_id_fkey", "medicine_outs",
        "ponds", ["pond_id"] , ["id"]
    )
   
    op.drop_table('medicine_medias')
    op.drop_table('pond_medias')
    op.drop_table('medias')
    pass


def downgrade():
    pass
