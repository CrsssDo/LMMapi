"""create table base season

Revision ID: 661366e29b38
Revises: c813b6b22d52
Create Date: 2022-07-04 10:51:47.036644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '661366e29b38'
down_revision = 'c813b6b22d52'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'purchasing_dealers',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String),
        sa.Column('name', sa.String),
        sa.Column('address', sa.String),
        sa.Column('address_level_1_id', sa.Integer),
        sa.ForeignKeyConstraint(['address_level_1_id'], ['address_level_1.id'])
    )
    op.create_table(
        'base_seasons',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('pond_id', sa.Integer, nullable=False),
        sa.Column('origin_fish_id', sa.Integer),
        sa.Column('supplier_id', sa.Integer),
        sa.Column('status', sa.String),
        sa.Column('in_date', sa.DATE),
        sa.Column('quantity', sa.Integer),
        sa.Column('density', sa.String),
        sa.Column('amount_of_quantity', sa.Integer),
        sa.Column('note', sa.String),
        sa.Column('comment', sa.String),
        sa.Column('water_index_poison', sa.String),
        sa.Column('supplier_address', sa.String),
        sa.Column('supplier_address_level_1_id', sa.Integer),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False),
        sa.ForeignKeyConstraint(['pond_id'], ['ponds.id']),
        sa.ForeignKeyConstraint(['origin_fish_id'], ['original_fishes.id']),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id']),
        sa.ForeignKeyConstraint(['supplier_address_level_1_id'], ['address_level_1.id'])
    )
    op.create_table(
        'collect_seasons',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('base_season_id', sa.Integer, nullable=False),
        sa.Column('purchasing_dealer_id', sa.Integer),
        sa.Column('start_date', sa.DateTime),
        sa.Column('finish_date', sa.DateTime),
        sa.Column('fish_size', sa.String),
        sa.Column('amount_of_collection', sa.Integer),
        sa.Column('purchasing_address', sa.String),
        sa.Column('purchasing_address_level_1_id', sa.Integer),
        sa.ForeignKeyConstraint(['base_season_id'], ['base_seasons.id']),
        sa.ForeignKeyConstraint(['purchasing_dealer_id'], ['purchasing_dealers.id']),
        sa.ForeignKeyConstraint(['purchasing_address_level_1_id'], ['address_level_1.id'])
    )
    op.create_table(
        'clean_seasons',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('base_season_id', sa.Integer, nullable=False),
        sa.Column('start_date', sa.DateTime),
        sa.Column('finish_date', sa.DateTime),
        sa.Column('process_description', sa.String),
        sa.Column('time_clear_pond', sa.String),
        sa.Column('time_between_season', sa.String),
        sa.Column('chemical_used', sa.String),
        sa.ForeignKeyConstraint(['base_season_id'], ['base_seasons.id'])
    )
    op.create_table(
        'water_index_seasons',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('base_season_id', sa.Integer, nullable=False),
        sa.Column('measure_index_id', sa.Integer),
        sa.Column('water_measure_value', sa.Float),
        sa.ForeignKeyConstraint(['base_season_id'], ['base_seasons.id']),
        sa.ForeignKeyConstraint(['measure_index_id'], ['measure_indexes.id'])
    )
    op.create_table(
        'history_status_seasons',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('base_season_id', sa.Integer, nullable=False),
        sa.Column('status', sa.String),
        sa.ForeignKeyConstraint(['base_season_id'], ['base_seasons.id'])
    )
    pass


def downgrade():
    op.drop_table('history_status_seasons')
    op.drop_table('water_index_seasons')
    op.drop_table('clean_seasons')
    op.drop_table('collect_seasons')
    op.drop_table('base_seasons')
    op.drop_table('purchasing_dealers')
    pass
