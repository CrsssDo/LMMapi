"""rename and drop table

Revision ID: 1c20c7b66ce1
Revises: 43b0e005b125
Create Date: 2022-06-01 13:13:56.662578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c20c7b66ce1'
down_revision = '43b0e005b125'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE food_in RENAME TO food_ins
    """)
    op.execute("""
    ALTER TABLE food_out RENAME TO food_outs
    """)
    op.execute("""
    ALTER TABLE medicine_in RENAME TO medicine_ins
    """)
    op.execute("""
    ALTER TABLE medicine_out RENAME TO medicine_outs
    """)
    op.execute("""
    ALTER TABLE fish_foods RENAME TO foods
    """)
    op.execute("""
    ALTER TABLE fish_diseases RENAME TO diseases
    """)
    pass
    


def downgrade():
    pass
