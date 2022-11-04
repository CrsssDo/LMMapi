"""add enum type role column into user table

Revision ID: aae5cf7076ab
Revises: 35a9aae87f8b
Create Date: 2022-06-06 09:19:18.298668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aae5cf7076ab'
down_revision = '35a9aae87f8b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        ALTER TABLE users ADD COLUMN role TEXT;

        CREATE TYPE roles 
        AS ENUM ('Super Admin', 'Administrator', 'Area Manager', 'Operator Manager', 'Operator', 'Technician Manager','Technician','Reporter');

        ALTER TABLE users ALTER COLUMN role TYPE roles USING role::roles;
    """)
    pass


def downgrade():
    op.execute("""
        ALTER TABLE users DROP IF EXISTS COLUMN role;
    """)
    pass
