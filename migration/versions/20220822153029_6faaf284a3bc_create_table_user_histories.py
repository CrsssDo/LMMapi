"""create table user histories

Revision ID: 6faaf284a3bc
Revises: ea242fd79003
Create Date: 2022-08-22 15:30:29.980922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6faaf284a3bc'
down_revision = 'ea242fd79003'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_histories',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('by_user_id', sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('record_type', sa.String(), nullable=False),
        sa.Column('record_id', sa.Integer(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )
    pass


def downgrade():
    op.drop_table('user_histories')
    pass
