"""create table pond categorizes

Revision ID: 9c41136a7ed2
Revises: 0f99721b6e28
Create Date: 2022-05-17 09:19:35.814286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c41136a7ed2'
down_revision = '0f99721b6e28'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pond_categorizes',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String, nullable=False)
    )
    op.execute("""
        INSERT INTO pond_categorizes(id, name) VALUES
        ('1','cá giống'),
        ('2','cá thịt'),
        ('3','ao bể xử lý nước')
        """)
    pass


def downgrade():
    op.drop_table('pond_categorizes')
    pass
