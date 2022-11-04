"""create table pond medias

Revision ID: fa52d6a7f5fc
Revises: 8ca5f415a498
Create Date: 2022-05-17 09:26:30.431148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa52d6a7f5fc'
down_revision = '8ca5f415a498'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pond_medias',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('pond_id', sa.Integer, nullable=False),
        sa.Column('pond_image_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['pond_id'], ['ponds.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pond_image_id'], ['medias.id'], ondelete='CASCADE'),
    )
    pass


def downgrade():
    op.drop_table('pond_medias')
    pass
