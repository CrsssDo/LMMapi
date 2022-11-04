"""add user admin

Revision ID: 109281d6a2f5
Revises: 6de310cefc20
Create Date: 2022-05-08 11:22:01.878239

"""
from alembic import op
import sqlalchemy as sa
from app.utils.password import hash


# revision identifiers, used by Alembic.
revision = '109281d6a2f5'
down_revision = '6de310cefc20'
branch_labels = None
depends_on = None


def upgrade():
    email = 'admin@nghenongviet.vn'
    password = hash('nnvadmin')
    op.execute(f"""
        INSERT INTO users(id, email, password)
        VALUES (1, '{email}', '{password}');
        """)


def downgrade():
      op.execute("""
        DELETE FROM users
        WHERE id = 1;
        """)
