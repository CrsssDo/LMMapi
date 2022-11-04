"""create table shape

Revision ID: e761744481a7
Revises: f6ef50ccbeda
Create Date: 2022-08-16 13:26:32.262931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e761744481a7'
down_revision = 'f6ef50ccbeda'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'shapes',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String),
        sa.Column('name', sa.String),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True))
        )
    op.execute("""
    INSERT INTO shapes(code, name)
    VALUES ('HT-01', 'Bao'),
           ('HT-02', 'Can'),
           ('HT-03', 'Bình'),
           ('HT-04', 'Túi'),
           ('HT-05', 'Chai')
    """)
    pass

def downgrade():
    op.drop_table('shapes')
    pass
