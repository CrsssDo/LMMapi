"""create table food type

Revision ID: 1c4888cf7154
Revises: e761744481a7
Create Date: 2022-08-17 13:56:12.058301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c4888cf7154'
down_revision = '6d3df373cfcb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'food_types',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String),
        sa.Column('name', sa.String),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True))
    )
    op.execute("""
        INSERT INTO food_types(code, name)
        VALUES ('LTA-01','Cá có vảy'),
               ('LTA-02','Cá da trơn')
    """)
    op.execute("""
        UPDATE foods
        SET type = 0
    """)
    op.execute("""
        ALTER TABLE foods
        ALTER COLUMN type TYPE int
        USING type::integer
    """)
    op.execute("""
        ALTER TABLE foods
        ADD COLUMN protein_value int,
        ADD COLUMN food_type_id int,
        ADD CONSTRAINT foods_food_type_id_fkey FOREIGN KEY(food_type_id) REFERENCES food_types(id)
    """)
    op.execute("""
        ALTER TABLE medicines
        ALTER COLUMN analysed_date DROP NOT NULL,
        ALTER COLUMN declared_date DROP NOT NULL
    """)
    pass


def downgrade():
    op.drop_table('food_types')
    pass

