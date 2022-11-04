"""create table adopt types

Revision ID: c2a2da52d82b
Revises: 8c1fd45a0273
Create Date: 2022-05-16 19:47:59.253948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2a2da52d82b'
down_revision = '8c1fd45a0273'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "adopt_area_types",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('current_timestamp'), nullable=False)
    )
    op.execute("""
        INSERT INTO adopt_area_types(id, name) VALUES
        (1, 'Vùng nuôi cá giống'),
        (2, 'Vùng nuôi cá thịt')
        """)
    pass


def downgrade():
    op.drop_table("adopt_area_types")
    pass
