"""add column unit_code into unit table

Revision ID: d70eddb87460
Revises: 6d3df373cfcb
Create Date: 2022-08-18 10:52:40.762796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd70eddb87460'
down_revision = '30d22e029bdc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('units', sa.Column('unit_code', sa.String()))
    op.drop_constraint('units_code_key','units')
    op.execute(f"""
        UPDATE units as u
        SET unit_code =  CONCAT('DV-','00', u.id)
        WHERE id < 10
    """)
    op.execute(f"""
        UPDATE units as u
        SET unit_code =  CONCAT('DV-','0', u.id)
        WHERE id < 100 and id >= 10
    """)
    op.execute(f"""
        UPDATE units as u
        SET unit_code =  CONCAT('DV-', u.id)
        WHERE id < 1000 and id >= 100
    """)
    pass


def downgrade():
    op.drop_column('units', 'unit_code')
    pass
