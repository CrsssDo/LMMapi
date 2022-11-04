"""add column code into table pong type

Revision ID: e846e3a5992b
Revises: 6faaf284a3bc
Create Date: 2022-08-24 10:19:39.525388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e846e3a5992b'
down_revision = '6faaf284a3bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pond_types', sa.Column('code', sa.String()))
    op.add_column('pond_types', sa.Column('symbol', sa.String()))
    op.add_column('pond_types', sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)))
    op.execute("""
        UPDATE pond_types
        SET code = 'LAB-01',
            name = 'Ao',
            symbol = 'A'
        WHERE pond_types.name = 'ao'
    """)
    op.execute("""
        UPDATE pond_types
        SET code = 'LAB-02',
            name = 'Bể',
            symbol = 'B'
        WHERE pond_types.name = 'bể'
    """)
    op.execute("""
        UPDATE pond_types
        SET code = 'LAB-03',
            name = 'Vèo',
            symbol = 'V'
        WHERE pond_types.name = 'vèo'
    """)
    op.add_column('ponds', sa.Column('number_order', sa.Integer()))
    op.execute("""
        UPDATE ponds as p
        SET code =  CONCAT('AB-','0',p.id)
        WHERE id < 10
    """)
    op.execute("""
        UPDATE ponds as p
        SET code =  CONCAT('AB-',p.id)
        WHERE id >= 10 and id < 100
    """)
    pass


def downgrade():
    op.drop_column('pond_types','code')
    op.drop_column('pond_types','symbol')
    op.drop_column('ponds', 'number_order')
    pass
