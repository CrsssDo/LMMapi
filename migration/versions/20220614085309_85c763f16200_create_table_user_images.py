"""create table user images

Revision ID: 85c763f16200
Revises: d6f69068bfb6
Create Date: 2022-06-14 08:53:09.630205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85c763f16200'
down_revision = 'd6f69068bfb6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('other_image_url', sa.String()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    pass


def downgrade():
    op.drop_table('user_images')
    pass
