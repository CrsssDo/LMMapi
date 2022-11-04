"""create table medias

Revision ID: 15f255ecd36c
Revises: 905b47d28c58
Create Date: 2022-05-17 09:13:27.516914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15f255ecd36c'
down_revision = '905b47d28c58'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'medias',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('file_name', sa.String, nullable=False),
        sa.Column('content_type', sa.String(55), nullable=False),
        sa.Column('file_url', sa.String, nullable=False),
        sa.Column('tail', sa.String(55), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('medias')
    pass
