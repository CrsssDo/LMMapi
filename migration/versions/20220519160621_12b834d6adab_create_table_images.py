"""create table images

Revision ID: 12b834d6adab
Revises: ee0d56fd56ec
Create Date: 2022-05-19 16:06:21.311475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12b834d6adab'
down_revision = 'ee0d56fd56ec'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'images',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('file_name', sa.String, nullable=False),
        sa.Column('ext', sa.String(55), nullable=False),
        sa.Column('url', sa.String, nullable=False),
        sa.Column('record_id', sa.Integer, nullable=False),
        sa.Column('record_type', sa.String, nullable=False),
        sa.Column('sub_type', sa.String),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('images')
    pass

