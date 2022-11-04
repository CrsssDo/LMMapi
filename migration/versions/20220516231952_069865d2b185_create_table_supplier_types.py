"""create_table_supplier_types

Revision ID: 069865d2b185
Revises: cc547b5a49f4
Create Date: 2022-05-16 23:19:52.267596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '069865d2b185'
down_revision = 'cc547b5a49f4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'supplier_types',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False)
        )
    op.execute("""
    INSERT INTO supplier_types(id,name) VALUES
    (1, 'NCC cá giống'),
    (2, 'NCC thức ăn'),
    (3, 'NCC thuốc')
    """)
    pass


def downgrade():
    op.drop_table('supplier_types')
    pass

