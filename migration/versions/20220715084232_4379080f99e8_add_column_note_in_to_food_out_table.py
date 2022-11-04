"""add column note in to food out table

Revision ID: 4379080f99e8
Revises: e5c3ad9eddac
Create Date: 2022-07-15 08:42:32.891061

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4379080f99e8'
down_revision = '46a391ed8223'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO supplier_types(id, name) VALUES
        (4, 'NNC hóa chất')
    """)
    op.execute("""
        ALTER TABLE food_outs
        ADD COLUMN note varchar
    """)
    op.execute("""
        ALTER TABLE medicine_outs
        ADD COLUMN note varchar
    """)
    op.execute("""
        UPDATE images
        SET sub_type = 'food_image'
        WHERE record_type = 'fish_foods'
    """)
    op.execute("""
        ALTER TABLE foods
        ADD COLUMN receiver_code varchar,
        ADD COLUMN uses varchar,
        ADD COLUMN element varchar,
        ADD COLUMN instructions_for_use varchar,
        ADD COLUMN status bool default true,
        ADD COLUMN supplier_id int,
        ADD COLUMN note varchar,
        ADD COLUMN analysed_date timestamp with time zone,
        ADD COLUMN declared_date timestamp with time zone
    """)
    op.add_column('foods', sa.Column('created_at', sa.TIMESTAMP(timezone=True),default=sa.text('now()'), server_default=sa.text('now()'), nullable=False))
    op.add_column('foods', sa.Column('updated_at', sa.TIMESTAMP(timezone=True),default=sa.text('now()'), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False))
    op.create_foreign_key(
        "foods_supplier_id_fkey", "foods",
        "suppliers", ["supplier_id"] , ["id"]
    )
    op.create_table(
        'chemistry_ins',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('batch_code', sa.String, nullable=False),
        sa.Column('chemistry_id', sa.Integer, nullable=False),
        sa.Column('adopt_area_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('inventory', sa.Integer, nullable=False),
        sa.Column('type_code', sa.String, nullable=False),
        sa.Column('in_date', sa.DATE, nullable=False),
        sa.Column('mfg_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('exp_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['chemistry_id'], ['chemistries.id']),
    )
    op.create_table(
        'chemistry_outs',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('chemistry_in_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Float, nullable=False),
        sa.Column('inventory', sa.Integer, nullable=False),
        sa.Column('note', sa.String),
        sa.Column('pond_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['chemistry_in_id'], ['chemistry_ins.id']),
        sa.ForeignKeyConstraint(['pond_id'], ['ponds.id']),
    )
    pass


def downgrade():
    op.drop_column(
        'food_outs',
        'note'
    )
    op.drop_column(
        'medicine_outs',
        'note'
    )
    op.execute("""
        ALTER TABLE foods
        DROP COLUMN receiver_code,
        DROP COLUMN uses,
        DROP COLUMN element,
        DROP COLUMN instructions_for_use,
        DROP COLUMN status,
        DROP COLUMN supplier_id,
        DROP COLUMN analysed_date,
        DROP COLUMN declared_date,
        DROP COLUMN created_at,
        DROP COLUMN updated_at
    """)
    op.drop_constraint(
        table_name='foods',
        constraint_name='foods_supplier_id_fkey'
    )
    op.drop_table('chemistry_outs')
    op.drop_table('chemistry_ins')
    pass
