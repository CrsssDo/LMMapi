"""create table medicine medias

Revision ID: ee0d56fd56ec
Revises: 6a0b794abed5
Create Date: 2022-05-18 13:58:50.222596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee0d56fd56ec'
down_revision = '6a0b794abed5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'medicine_medias',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('medicine_id', sa.Integer, nullable=False),
        sa.Column('medicine_image_id', sa.Integer),
        sa.Column('certificate_image_id', sa.Integer),
        sa.ForeignKeyConstraint(['medicine_id'], ['medicines.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['medicine_image_id'], ['medias.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['certificate_image_id'], ['medias.id'], ondelete='CASCADE')
    )
    pass


def downgrade():
    op.drop_table('medicine_medias')
    pass
