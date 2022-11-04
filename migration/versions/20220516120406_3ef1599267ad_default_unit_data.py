"""default unit data

Revision ID: 3ef1599267ad
Revises: 61a8e58e1a52
Create Date: 2022-05-16 12:04:06.507625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ef1599267ad'
down_revision = '61a8e58e1a52'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    INSERT INTO units(id,code, description)
    VALUES (1,'kg','kilogram'),
           (2,'g','gram'),
           (3,'mg/l','miligram/lít'),
           (4,'k','kelvin (Độ K)'),
           (5,'mol','mole (hàm lượng của 1 chất)'),
           (6,'km','kilometer'),
           (7,'m','meter'),
           (8,'m3','cubic meter'),
           (9,'con','số con cá'),
           (10,'con/m3','số cá/m3')
    """
    )
    pass


def downgrade():
    pass
