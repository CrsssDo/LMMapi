"""create table pond type

Revision ID: 0f99721b6e28
Revises: 15f255ecd36c
Create Date: 2022-05-17 09:13:33.378167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f99721b6e28'
down_revision = '15f255ecd36c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pond_types',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String, nullable=False)
    )
    op.execute("""
    INSERT INTO pond_types(id, name) VALUES
    ('1','ao'),
    ('2','bể'),
    ('3','vèo')
    """)
    pass


def downgrade():
    op.drop_table('pond_types')
    pass
