"""add address adopt code full_name column into user table

Revision ID: d6f69068bfb6
Revises: 882c3d0d4aad
Create Date: 2022-06-09 15:21:13.765186

"""
from alembic import op
import sqlalchemy as sa
from app.utils.password import hash



# revision identifiers, used by Alembic.
revision = 'd6f69068bfb6'
down_revision = '882c3d0d4aad'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        ALTER TABLE users
        ADD COLUMN code varchar(15) NOT NULL DEFAULT 'not set',
        ADD COLUMN full_name varchar(255) NOT NULL DEFAULT 'not set',
        ADD COLUMN phone varchar(10) NOT NULL DEFAULT 'not set',
        ADD COLUMN role varchar(255) NOT NULL DEFAULT 'not set',
        ADD COLUMN address varchar(50) NOT NULL DEFAULT 'not set',
        ADD COLUMN avatar_image_url varchar,
        ADD COLUMN before_identity_image_url varchar,
        ADD COLUMN after_identity_image_url varchar,
        ADD COLUMN adopt_area_id int,
        ADD COLUMN address_level_1_id int NOT NULL DEFAULT 1
        """)
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN code DROP DEFAULT,
        ALTER COLUMN full_name DROP DEFAULT,
        ALTER COLUMN phone DROP DEFAULT,
        ALTER COLUMN role DROP DEFAULT,
        ALTER COLUMN address DROP DEFAULT,
        ALTER COLUMN address_level_1_id DROP DEFAULT
        """)
    op.execute("""
    ALTER TABLE users
    ADD CONSTRAINT users_adopt_area_id_fkey FOREIGN KEY(adopt_area_id) REFERENCES adopt_areas(id),
    ADD CONSTRAINT users_address_level_1_id_fkey FOREIGN KEY(address_level_1_id) REFERENCES address_level_1(id)
    """)
    pass


def downgrade():
    op.execute("""
        ALTER TABLE users
        DROP COLUMN code,
        DROP COLUMN full_name,
        DROP COLUMN phone,
        DROP COLUMN role,
        DROP COLUMN address,
        DROP COLUMN avatar_image_url,
        DROP COLUMN before_identity_image_url,
        DROP COLUMN after_identity_image_url,
        DROP COLUMN adopt_area_id,
        DROP COLUMN address_level_1_id;
        """)
    op.drop_constraint(
        table_name='users',
        constraint_name='users_adopt_area_id_fkey'
    )
    op.drop_constraint(
        table_name='users',
        constraint_name='users_address_level_1_id_fkey'
    )
    pass
