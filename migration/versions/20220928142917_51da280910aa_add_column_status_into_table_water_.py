"""add column status into table water diary detail

Revision ID: 51da280910aa
Revises: 9462e98c3328
Create Date: 2022-09-28 14:29:17.249708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51da280910aa'
down_revision = '9462e98c3328'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        TRUNCATE TABLE clean_seasons
        RESTART IDENTITY
    """)
    op.execute("""
        TRUNCATE TABLE collect_seasons
        RESTART IDENTITY
    """)
    op.execute("""
        TRUNCATE TABLE base_season_ponds
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE base_seasons
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE history_status_seasons
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE water_diaries_detail
        RESTART IDENTITY
    """)
    op.execute("""
        TRUNCATE TABLE water_diaries
        RESTART IDENTITY CASCADE
    """)
    op.execute("""
        TRUNCATE TABLE water_index_seasons
        RESTART IDENTITY
    """)
    op.add_column('water_diaries_detail', sa.Column('status', sa.Boolean(), default=True))
    op.add_column('water_index_seasons', sa.Column('status', sa.Boolean(), default=True))
    op.create_table(
        'water_diary_histories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('water_diary_id', sa.Integer),
        sa.Column('measure_index_id', sa.Integer),
        sa.Column('measure_value', sa.Float),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False),
        sa.ForeignKeyConstraint(['water_diary_id'], ['water_diaries.id']),
        sa.ForeignKeyConstraint(['measure_index_id'], ['measure_indexes.id'])
    )

    pass


def downgrade():
    pass
