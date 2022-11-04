"""create_table_address_level_3

Revision ID: f809792baba0
Revises: 3ef1599267ad
Create Date: 2022-05-16 15:51:10.505051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f809792baba0'
down_revision = '3ef1599267ad'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'address_level_3',
        sa.Column('id',sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(255))
    )
    op.execute("""
    INSERT INTO address_level_3 (id, name) VALUES
	(1, 'Tỉnh An Giang'),
	(2, 'Tỉnh Bà Rịa - Vũng Tàu'),
	(3, 'Tỉnh Bạc Liêu'),
	(4, 'Tỉnh Bến Tre'),
	(5, 'Tỉnh Bình Dương'),
	(6, 'Tỉnh Bình Phước'),
	(7, 'Tỉnh Cà Mau'),
	(8, 'Thành Phố Cần Thơ'),
	(9, 'Tỉnh Đồng Nai'),
	(10, 'Tỉnh Đồng Tháp'),
	(11, 'Tỉnh Hậu Giang'),
	(12, 'Thành Phố Hồ Chí Minh'),
	(13, 'Tỉnh Kiên Giang'),
	(14, 'Tỉnh Long An'),
	(15, 'Tỉnh Sóc Trăng'),
	(16, 'Tỉnh Tây Ninh'),
	(17, 'Tỉnh Tiền Giang'),
	(18, 'Tỉnh Trà Vinh'),
	(19, 'Tỉnh Vĩnh Long'),
	(20, 'Thành phố Đà Nẵng'),
	(21, 'Thành phố Hà Nội'),
	(22, 'Thành phố Hải Phòng'),
	(23, 'Tỉnh Bắc Giang'),
	(24, 'Tỉnh Bắc Kạn'),
	(25, 'Tỉnh Bắc Ninh'),
	(26, 'Tỉnh Bình Định'),
	(27, 'Tỉnh Bình Thuận'),
	(28, 'Tỉnh Cao Bằng'),
	(29, 'Tỉnh Đắk Lắk'),
	(30, 'Tỉnh Đắk Nông'),
	(31, 'Tỉnh Điện Biên'),
	(32, 'Tỉnh Gia Lai'),
	(33, 'Tỉnh Hà Giang'),
	(34, 'Tỉnh Hà Nam'),
	(35, 'Tỉnh Hà Tĩnh'),
	(36, 'Tỉnh Hải Dương'),
	(37, 'Tỉnh Hoà Bình'),
	(38, 'Tỉnh Hưng Yên'),
	(39, 'Tỉnh Khánh Hòa'),
	(40, 'Tỉnh Kon Tum'),
	(41, 'Tỉnh Lai Châu'),
	(42, 'Tỉnh Lâm Đồng'),
	(43, 'Tỉnh Lạng Sơn'),
	(44, 'Tỉnh Lào Cai'),
	(45, 'Tỉnh Nam Định'),
	(46, 'Tỉnh Nghệ An'),
	(47, 'Tỉnh Ninh Bình'),
	(48, 'Tỉnh Ninh Thuận'),
	(49, 'Tỉnh Phú Thọ'),
	(50, 'Tỉnh Phú Yên'),
	(51, 'Tỉnh Quảng Bình'),
	(52, 'Tỉnh Quảng Nam'),
	(53, 'Tỉnh Quảng Ngãi'),
	(54, 'Tỉnh Quảng Ninh'),
	(55, 'Tỉnh Quảng Trị'),
	(56, 'Tỉnh Sơn La'),
	(57, 'Tỉnh Thái Bình'),
	(58, 'Tỉnh Thái Nguyên'),
	(59, 'Tỉnh Thanh Hóa'),
	(60, 'Tỉnh Thừa Thiên Huế'),
	(61, 'Tỉnh Tuyên Quang'),
	(62, 'Tỉnh Vĩnh Phúc'),
	(63, 'Tỉnh Yên Bái')
    """)
    pass


def downgrade():
    op.drop_table('address_level_3')
    pass
