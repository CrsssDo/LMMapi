"""add column specification_id into food in table

Revision ID: ea242fd79003
Revises: d70eddb87460
Create Date: 2022-08-19 15:36:34.098616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea242fd79003'
down_revision = 'd70eddb87460'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('food_ins', sa.Column('specification_id', sa.Integer))
    op.execute("""
        ALTER TABLE food_ins
        ADD CONSTRAINT food_ins_specification_id_fkey FOREIGN KEY(specification_id) REFERENCES specifications(id)
    """)
    op.add_column('medicine_ins', sa.Column('specification_id', sa.Integer))
    op.execute("""
        ALTER TABLE medicine_ins
        ADD CONSTRAINT medicine_ins_specification_id_fkey FOREIGN KEY(specification_id) REFERENCES specifications(id)
    """)
    op.add_column('chemistry_ins', sa.Column('specification_id', sa.Integer))
    op.execute("""
        ALTER TABLE chemistry_ins
        ADD CONSTRAINT chemistry_ins_specification_id_fkey FOREIGN KEY(specification_id) REFERENCES specifications(id)
    """)
    op.create_table(
        'medicine_types',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String),
        sa.Column('name', sa.String),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True))
    )
    op.execute("""
        ALTER TABLE medicines
        ALTER COLUMN medicine_type DROP NOT NULL,
        ADD COLUMN medicine_type_id int,
        ADD CONSTRAINT medicines_medicine_type_id_fkey FOREIGN KEY(medicine_type_id) REFERENCES medicine_types(id)
    """)
    op.create_table(
        'chemistry_types',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String),
        sa.Column('name', sa.String),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True))
    )
    op.execute("""
        ALTER TABLE chemistries
        ADD COLUMN chemistry_type_id int,
        ADD CONSTRAINT chemistries_chemistry_type_id_fkey FOREIGN KEY(chemistry_type_id) REFERENCES chemistry_types(id)
    """)
    pass


def downgrade():
    op.drop_column('food_ins','specification_id')
    op.drop_column('medicine_ins','specification_id')
    op.drop_column('chemistry_ins','specification_id')
    op.drop_table('medicine_types')
    op.drop_table('chemistry_types')
    pass
