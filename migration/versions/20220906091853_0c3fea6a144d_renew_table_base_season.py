"""renew table base season

Revision ID: 0c3fea6a144d
Revises: 453cd9fbcd48
Create Date: 2022-09-06 09:18:53.151701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c3fea6a144d'
down_revision = '453cd9fbcd48'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('base_seasons','base_season_ponds')
    op.create_table(
        'base_seasons',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String),
        sa.Column('status', sa.String),
        sa.Column('adopt_area_id', sa.Integer),
        sa.Column('notes', sa.String(500)),
        sa.Column('expected_start_date', sa.DateTime()),
        sa.Column('expected_end_date', sa.DateTime()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False),
        sa.ForeignKeyConstraint(['adopt_area_id'], ['adopt_areas.id'])
    )
    op.execute("""
        ALTER TABLE base_season_ponds
        ADD COLUMN base_season_id int,
        ADD CONSTRAINT base_season_ponds_base_season_id_fkey FOREIGN KEY(base_season_id) REFERENCES base_seasons(id)
    """)
    op.execute("""
        ALTER TABLE collect_seasons
        RENAME COLUMN base_season_id TO base_season_pond_id
    """)
    op.execute("""
        ALTER TABLE clean_seasons
        RENAME COLUMN base_season_id TO base_season_pond_id
    """)
    op.execute("""
        ALTER TABLE history_status_seasons
        RENAME COLUMN base_season_id TO base_season_pond_id
    """)
    op.execute("""
        ALTER TABLE water_index_seasons
        RENAME COLUMN base_season_id TO base_season_pond_id
    """)
    op.execute("""
        ALTER TABLE collect_seasons
        ADD CONSTRAINT collect_seasons_base_season_pond_id_fkey FOREIGN KEY(base_season_pond_id) REFERENCES base_season_ponds(id)
    """)
    op.execute("""
        ALTER TABLE clean_seasons
        ADD CONSTRAINT clean_seasons_base_season_pond_id_fkey FOREIGN KEY(base_season_pond_id) REFERENCES base_season_ponds(id)
    """)
    op.execute("""
        ALTER TABLE history_status_seasons
        ADD CONSTRAINT history_status_seasons_base_season_pond_id_fkey FOREIGN KEY(base_season_pond_id) REFERENCES base_season_ponds(id)
    """)
    op.execute("""
        ALTER TABLE water_index_seasons
        ADD CONSTRAINT water_index_seasons_base_season_pond_id_fkey FOREIGN KEY(base_season_pond_id) REFERENCES base_season_ponds(id)
    """)
    pass


def downgrade():
    pass
