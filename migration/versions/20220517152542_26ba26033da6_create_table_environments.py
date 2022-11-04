"""create table environments

Revision ID: 26ba26033da6
Revises: 2ef7b8dce42f
Create Date: 2022-05-17 15:25:42.134410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26ba26033da6'
down_revision = '2ef7b8dce42f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'environments',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False)
    )
    op.execute("""
    INSERT INTO environments(id, code, name) VALUES
    ('1','PH','Độ kiềm'),
    ('2','oC','Nhiệt độ'),
    ('3','mg/L','Oxy-DO'),
    ('4','H2S','Axit Hydro sulfua'),
    ('5','NH3','Amoniac')
    """)
    pass


def downgrade():
    op.drop_table('environments')
    pass
