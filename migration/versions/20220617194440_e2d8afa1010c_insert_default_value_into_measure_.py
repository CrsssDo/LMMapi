"""insert default value into measure_indexes

Revision ID: e2d8afa1010c
Revises: 8720791a1220
Create Date: 2022-06-17 19:44:40.050011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2d8afa1010c'
down_revision = '8720791a1220'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    TRUNCATE measure_indexes RESTART IDENTITY
    """)
    op.execute("""
    ALTER TABLE measure_indexes 
    ALTER COLUMN unit_id DROP NOT NULL
    """)
    op.execute("""
    ALTER TABLE measure_indexes
    ADD COLUMN status boolean DEFAULT TRUE
    """)
    op.execute("""
    INSERT INTO measure_indexes(id, code, max_range, min_range, water_environment, unit_id, status)
    VALUES  (1, 'DO', null, 2, 'Nước ngọt', 3, true),
            (2, 'pH', 9, 7, 'Nước ngọt', null, true),
            (3, 'Nhiệt độ', 32, 25, 'Nước ngọt', null, true),
            (4, 'NH3', 0.3 , null, 'Nước ngọt', 3, true),
            (5, 'Độ kiềm', 180, 60, 'Nước ngọt', null, true),
            (6, 'H2S', 0.05 , null, 'Nước ngọt', 3, true),
            (7, 'NO2', null, null, 'Nước ngọt', null, true)
    """)
    op.execute("""
    UPDATE users
    SET code = 'NNV-0001', full_name = 'Super Admin'
    WHERE id = 1
    """)
    pass


def downgrade():
    op.drop_column(
        'measure_indexes',
        'status'
    )
    op.execute("""
    DELETE FROM measure_indexes WHERE id = 1;
    DELETE FROM measure_indexes WHERE id = 2;
    DELETE FROM measure_indexes WHERE id = 3;
    DELETE FROM measure_indexes WHERE id = 4;
    DELETE FROM measure_indexes WHERE id = 5;
    DELETE FROM measure_indexes WHERE id = 6;
    DELETE FROM measure_indexes WHERE id = 7;
    """)
    pass
