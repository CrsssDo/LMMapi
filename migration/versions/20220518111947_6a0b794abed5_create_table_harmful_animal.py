"""create table harmful animal

Revision ID: 6a0b794abed5
Revises: cfed8e8b9aef
Create Date: 2022-05-18 11:19:47.398724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a0b794abed5'
down_revision = 'cfed8e8b9aef'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'harmful_animals',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('harmful_animals')
    pass
