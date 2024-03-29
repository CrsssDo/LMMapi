"""create_address_level_2

Revision ID: 4471c3da2a15
Revises: f809792baba0
Create Date: 2022-05-16 15:55:03.305517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4471c3da2a15'
down_revision = 'f809792baba0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'address_level_2',
        sa.Column('id',sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(255)),
        sa.Column('address_level_3_id', sa.Integer()),
        sa.ForeignKeyConstraint(['address_level_3_id'], ['address_level_3.id'], ondelete='SET NULL')
    )
    op.execute("""
    INSERT INTO address_level_2 (id, name, address_level_3_id) VALUES
	(1, 'Huyện Phú Tân', 1),
	(2, 'Thành Phố Châu Đốc', 1),
	(3, 'Huyện Tri Tôn', 1),
	(4, 'Thành Phố Long Xuyên', 1),
	(5, 'Huyện An Phú', 1),
	(6, 'Huyện Tịnh Biên', 1),
	(7, 'Huyện Chợ Mới', 1),
	(8, 'Huyện Thoại Sơn', 1),
	(9, 'Huyện Châu Thành', 1),
	(10, 'Thị Xã Tân Châu', 1),
	(11, 'Huyện Châu Phú', 1),
	(12, 'Thị Xã Phú Mỹ', 2),
	(13, 'Huyện Long Điền', 2),
	(14, 'Huyện Xuyên Mộc', 2),
	(15, 'Huyện Đất Đỏ', 2),
	(16, 'Thành Phố Vũng Tàu', 2),
	(17, 'Huyện Châu Đức', 2),
	(18, 'Huyện Tân Thành', 2),
	(19, 'Thành Phố Bà Rịa', 2),
	(20, 'Huyện Đông Hải', 3),
	(21, 'Huyện Phước Long', 3),
	(22, 'Thành Phố Bạc Liêu', 3),
	(23, 'Huyện Hồng Dân', 3),
	(24, 'Huyện Hòa Bình', 3),
	(25, 'Thị Xã Giá Rai', 3),
	(26, 'Huyện Vĩnh Lợi', 3),
	(27, 'Huyện Châu Thành', 4),
	(28, 'Huyện Mỏ Cày Nam', 4),
	(29, 'Huyện Bình Đại', 4),
	(30, 'Huyện Mỏ Cày Bắc', 4),
	(31, 'Thành Phố Bến Tre', 4),
	(32, 'Huyện Giồng Trôm', 4),
	(33, 'Huyện Ba Tri', 4),
	(34, 'Huyện Chợ Lách', 4),
	(35, 'Huyện Thạnh Phú', 4),
	(36, 'Huyện Dầu Tiếng', 5),
	(37, 'Thành Phố Thủ Dầu Một', 5),
	(38, 'Thị Xã Bến Cát', 5),
	(39, 'Thị Xã Tân Uyên', 5),
	(40, 'Huyện Bàu Bàng', 5),
	(41, 'Huyện Phú Giáo', 5),
	(42, 'Huyện Bắc Tân Uyên', 5),
	(43, 'Thành Phố Dĩ An', 5),
	(44, 'Thành Phố Thuận An', 5),
	(45, 'Huyện Lộc Ninh', 6),
	(46, 'Huyện Bù Gia Mập', 6),
	(47, 'Huyện Hớn Quản', 6),
	(48, 'Huyện Bù Đốp', 6),
	(49, 'Thành Phố Đồng Xoài', 6),
	(50, 'Huyện Bù Đăng', 6),
	(51, 'Thị Xã Phước Long', 6),
	(52, 'Huyện Đồng Phú', 6),
	(53, 'Thị Xã Bình Long', 6),
	(54, 'Huyện Phú Riềng', 6),
	(55, 'Huyện Chơn Thành', 6),
	(56, 'Huyện Thới Bình', 7),
	(57, 'Huyện Cái Nước', 7),
	(58, 'Huyện Phú Tân', 7),
	(59, 'Thành Phố Cà Mau', 7),
	(60, 'Huyện Ngọc Hiển', 7),
	(61, 'Huyện U Minh', 7),
	(62, 'Huyện Năm Căn', 7),
	(63, 'Huyện Trần Văn Thời', 7),
	(64, 'Huyện Đầm Dơi', 7),
	(65, 'Huyện Thới Lai', 8),
	(66, 'Quận Cái Răng', 8),
	(67, 'Huyện Phong Điền', 8),
	(68, 'Quận Bình Thủy', 8),
	(69, 'Quận Ô Môn', 8),
	(70, 'Huyện Vĩnh Thạnh', 8),
	(71, 'Quận Ninh Kiều', 8),
	(72, 'Quận Thốt Nốt', 8),
	(73, 'Huyện Cờ Đỏ', 8),
	(74, 'Huyện Tân Phú', 9),
	(75, 'Huyện Cẩm Mỹ', 9),
	(76, 'Huyện Xuân Lộc', 9),
	(77, 'Huyện Nhơn Trạch', 9),
	(78, 'Thành Phố Biên Hòa', 9),
	(79, 'Huyện Vĩnh Cửu', 9),
	(80, 'Huyện Long Thành', 9),
	(81, 'Huyện Trảng Bom', 9),
	(82, 'Thành Phố Long Khánh', 9),
	(83, 'Huyện Thống Nhất', 9),
	(84, 'Huyện Định Quán', 9),
	(85, 'Thành Phố Cao Lãnh', 10),
	(86, 'Huyện Tháp Mười', 10),
	(87, 'Huyện Lấp Vò', 10),
	(88, 'Huyện Thanh Bình', 10),
	(89, 'Huyện Lai Vung', 10),
	(90, 'Huyện Tân Hồng', 10),
	(91, 'Thành Phố Hồng Ngự', 10),
	(92, 'Huyện Tam Nông', 10),
	(93, 'Huyện Châu Thành', 10),
	(94, 'Thành Phố Sa Đéc', 10),
	(95, 'Thành Phố Ngã Bảy', 11),
	(96, 'Thị Xã Long Mỹ', 11),
	(97, 'Huyện Vị Thủy', 11),
	(98, 'Huyện Châu Thành A', 11),
	(99, 'Thành Phố Vị Thanh', 11),
	(100, 'Huyện Châu Thành', 11),
	(101, 'Huyện Phụng Hiệp', 11),
	(102, 'Huyện Cần Giờ', 12),
	(103, 'Quận 2', 12),
	(104, 'Quận 11', 12),
	(105, 'Huyện Nhà Bè', 12),
	(106, 'Quận 6', 12),
	(107, 'Quận Bình Thạnh', 12),
	(108, 'Quận Thủ Đức', 12),
	(109, 'Quận 1', 12),
	(110, 'Quận 10', 12),
	(111, 'Huyện Hóc Môn', 12),
	(112, 'Quận 5', 12),
	(113, 'Quận Bình Tân', 12),
	(114, 'Quận Tân Phú', 12),
	(115, 'Quận 9', 12),
	(116, 'Quận Gò Vấp', 12),
	(117, 'Quận 4', 12),
	(118, 'Huyện Bình Chánh', 12),
	(119, 'Quận Tân Bình', 12),
	(120, 'Quận 8', 12),
	(121, 'Huyện Củ Chi', 12),
	(122, 'Quận 3', 12),
	(123, 'Quận 12', 12),
	(124, 'Quận Phú Nhuận', 12),
	(125, 'Quận 7', 12),
	(126, 'Huyện An Biên', 13),
	(127, 'Thành Phố Rạch Giá', 13),
	(128, 'Huyện Giồng Riềng', 13),
	(129, 'Huyện Kiên Lương', 13),
	(130, 'Huyện Giang Thành', 13),
	(131, 'Huyện Vĩnh Thuận', 13),
	(132, 'Huyện Hòn Đất', 13),
	(133, 'Huyện Châu Thành', 13),
	(134, 'Huyện U Minh Thượng', 13),
	(135, 'Thành Phố Hà Tiên', 13),
	(136, 'Huyện An Minh', 13),
	(137, 'Huyện Tân Hiệp', 13),
	(138, 'Huyện Gò Quao', 13),
	(139, 'Huyện Tân Thạnh', 14),
	(140, 'Huyện Đức Huệ', 14),
	(141, 'Huyện Vĩnh Hưng', 14),
	(142, 'Huyện Bến Lức', 14),
	(143, 'Huyện Tân Hưng', 14),
	(144, 'Huyện Đức Hòa', 14),
	(145, 'Huyện Thủ Thừa', 14),
	(146, 'Thành Phố Tân An', 14),
	(147, 'Huyện Châu Thành', 14),
	(148, 'Huyện Thạnh Hóa', 14),
	(149, 'Huyện Mộc Hóa', 14),
	(150, 'Huyện Cần Giuộc', 14),
	(151, 'Huyện Tân Trụ', 14),
	(152, 'Thị Xã Kiến Tường', 14),
	(153, 'Huyện Cần Đước', 14),
	(154, 'Huyện Mỹ Tú', 15),
	(155, 'Huyện Thạnh Trị', 15),
	(156, 'Huyện Long Phú', 15),
	(157, 'Thành Phố Sóc Trăng', 15),
	(158, 'Huyện Kế Sách', 15),
	(159, 'Thị Xã Ngã Năm', 15),
	(160, 'Huyện Cù Lao Dung', 15),
	(161, 'Thị Xã Vĩnh Châu', 15),
	(162, 'Huyện Mỹ Xuyên', 15),
	(163, 'Huyện Châu Thành', 15),
	(164, 'Huyện Trần Đề', 15),
	(165, 'Huyện Dương Minh Châu', 16),
	(166, 'Huyện Tân Châu', 16),
	(167, 'Huyện Châu Thành', 16),
	(168, 'Huyện Tân Biên', 16),
	(169, 'Huyện Bến Cầu', 16),
	(170, 'Huyện Hòa Thành', 16),
	(171, 'Huyện Trảng Bàng', 16),
	(172, 'Huyện Gò Dầu', 16),
	(173, 'Thành Phố Tây Ninh', 16),
	(174, 'Thành Phố Mỹ Tho', 17),
	(175, 'Huyện Châu Thành', 17),
	(176, 'Huyện Gò Công Tây', 17),
	(177, 'Thị Xã Cai Lậy', 17),
	(178, 'Huyện Gò Công Đông', 17),
	(179, 'Huyện Cái Bè', 17),
	(180, 'Huyện Tân Phước', 17),
	(181, 'Thị Xã Gò Công', 17),
	(182, 'Huyện Tân Phú Đông', 17),
	(183, 'Huyện Chợ Gạo', 17),
	(184, 'Huyện Trà Cú', 18),
	(185, 'Huyện Cầu Kè', 18),
	(186, 'Huyện Tiểu Cần', 18),
	(187, 'Huyện Càng Long', 18),
	(188, 'Thị Xã Duyên Hải', 18),
	(189, 'Huyện Châu Thành', 18),
	(190, 'Thành Phố Trà Vinh', 18),
	(191, 'Huyện Cầu Ngang', 18),
	(192, 'Huyện Vũng Liêm', 19),
	(193, 'Huyện Long Hồ', 19),
	(194, 'Thành Phố Vĩnh Long', 19),
	(195, 'Huyện Bình Tân', 19),
	(196, 'Huyện Trà Ôn', 19),
	(197, 'Thị Xã Bình Minh', 19),
	(198, 'Huyện Tam Bình', 19),
	(199, 'Huyện Mang Thít', 19),
	(200, 'Thành Phố Phú Quốc', 13),
	(201, 'Huyện Kiên Hải', 13),
	(202, 'Huyện Hòa Vang', 20),
	(203, 'Quận Cẩm Lệ', 20),
	(204, 'Quận Hải Châu', 20),
	(205, 'Quận Liên Chiểu', 20),
	(206, 'Quận Ngũ Hành Sơn', 20),
	(207, 'Quận Sơn Trà', 20),
	(208, 'Quận Thanh Khê', 20),
	(209, 'Huyện Ba Vì', 21),
	(210, 'Huyện Chương Mỹ', 21),
	(211, 'Huyện Đan Phượng', 21),
	(212, 'Huyện Đông Anh', 21),
	(213, 'Huyện Gia Lâm', 21),
	(214, 'Huyện Hoài Đức', 21),
	(215, 'Huyện Mê Linh', 21),
	(216, 'Huyện Mỹ Đức', 21),
	(217, 'Huyện Phú Xuyên', 21),
	(218, 'Huyện Phúc Thọ', 21),
	(219, 'Huyện Quốc Oai', 21),
	(220, 'Huyện Sóc Sơn', 21),
	(221, 'Huyện Thạch Thất', 21),
	(222, 'Huyện Thanh Oai', 21),
	(223, 'Huyện Thanh Trì', 21),
	(224, 'Huyện Thường Tín', 21),
	(225, 'Huyện Ứng Hòa', 21),
	(226, 'Quận Ba Đình', 21),
	(227, 'Quận Bắc Từ Liêm', 21),
	(228, 'Quận Cầu Giấy', 21),
	(229, 'Quận Đống Đa', 21),
	(230, 'Quận Hà Đông', 21),
	(231, 'Quận Hai Bà Trưng', 21),
	(232, 'Quận Hoàn Kiếm', 21),
	(233, 'Quận Hoàng Mai', 21),
	(234, 'Quận Long Biên', 21),
	(235, 'Quận Nam Từ Liêm', 21),
	(236, 'Quận Tây Hồ', 21),
	(237, 'Quận Thanh Xuân', 21),
	(238, 'Thị xã Sơn Tây', 21),
	(239, 'Huyện An Dương', 22),
	(240, 'Huyện An Lão', 22),
	(241, 'Huyện Cát Hải', 22),
	(242, 'Huyện Kiến Thuỵ', 22),
	(243, 'Huyện Thuỷ Nguyên', 22),
	(244, 'Huyện Tiên Lãng', 22),
	(245, 'Huyện Vĩnh Bảo', 22),
	(246, 'Quận Dương Kinh', 22),
	(247, 'Quận Đồ Sơn', 22),
	(248, 'Quận Hải An', 22),
	(249, 'Quận Hồng Bàng', 22),
	(250, 'Quận Kiến An', 22),
	(251, 'Quận Lê Chân', 22),
	(252, 'Quận Ngô Quyền', 22),
	(253, 'Huyện Hiệp Hòa', 23),
	(254, 'Huyện Lạng Giang', 23),
	(255, 'Huyện Lục Nam', 23),
	(256, 'Huyện Lục Ngạn', 23),
	(257, 'Huyện Sơn Động', 23),
	(258, 'Huyện Tân Yên', 23),
	(259, 'Huyện Việt Yên', 23),
	(260, 'Huyện Yên Dũng', 23),
	(261, 'Huyện Yên Thế', 23),
	(262, 'Thành phố Bắc Giang', 23),
	(263, 'Huyện Ba Bể', 24),
	(264, 'Huyện Bạch Thông', 24),
	(265, 'Huyện Chợ Đồn', 24),
	(266, 'Huyện Chợ Mới', 24),
	(267, 'Huyện Na Rì', 24),
	(268, 'Huyện Ngân Sơn', 24),
	(269, 'Huyện Pác Nặm', 24),
	(270, 'Thành Phố Bắc Kạn', 24),
	(271, 'Huyện Gia Bình', 25),
	(272, 'Huyện Lương Tài', 25),
	(273, 'Huyện Quế Võ', 25),
	(274, 'Huyện Thuận Thành', 25),
	(275, 'Huyện Tiên Du', 25),
	(276, 'Huyện Yên Phong', 25),
	(277, 'Thành phố Bắc Ninh', 25),
	(278, 'Thành phố Từ Sơn', 25),
	(279, 'Huyện An Lão', 26),
	(280, 'Huyện Hoài Ân', 26),
	(281, 'Huyện Phù Cát', 26),
	(282, 'Huyện Phù Mỹ', 26),
	(283, 'Huyện Tây Sơn', 26),
	(284, 'Huyện Tuy Phước', 26),
	(285, 'Huyện Vân Canh', 26),
	(286, 'Huyện Vĩnh Thạnh', 26),
	(287, 'Thành phố Quy Nhơn', 26),
	(288, 'Thị xã An Nhơn', 26),
	(289, 'Thị xã Hoài Nhơn', 26),
	(290, 'Huyện Bắc Bình', 27),
	(291, 'Huyện Đức Linh', 27),
	(292, 'Huyện Hàm Tân', 27),
	(293, 'Huyện Hàm Thuận Bắc', 27),
	(294, 'Huyện Hàm Thuận Nam', 27),
	(295, 'Huyện Phú Quí', 27),
	(296, 'Huyện Tánh Linh', 27),
	(297, 'Huyện Tuy Phong', 27),
	(298, 'Thành phố Phan Thiết', 27),
	(299, 'Thị xã La Gi', 27),
	(300, 'Huyện Bảo Lạc', 28),
	(301, 'Huyện Bảo Lâm', 28),
	(302, 'Huyện Hạ Lang', 28),
	(303, 'Huyện Hà Quảng', 28),
	(304, 'Huyện Hoà An', 28),
	(305, 'Huyện Nguyên Bình', 28),
	(306, 'Huyện Quảng Hòa', 28),
	(307, 'Huyện Thạch An', 28),
	(308, 'Huyện Trùng Khánh', 28),
	(309, 'Thành phố Cao Bằng', 28),
	(310, 'Huyện Buôn Đôn', 29),
	(311, 'Huyện Cư Kuin', 29),
	(312, 'Huyện Cư M gar', 29),
	(313, 'Huyện Ea H leo', 29),
	(314, 'Huyện Ea Kar', 29),
	(315, 'Huyện Ea Súp', 29),
	(316, 'Huyện Krông A Na', 29),
	(317, 'Huyện Krông Bông', 29),
	(318, 'Huyện Krông Búk', 29),
	(319, 'Huyện Krông Năng', 29),
	(320, 'Huyện Krông Pắc', 29),
	(321, 'Huyện Lắk', 29),
	(322, 'Huyện M Đrắk', 29),
	(323, 'Thành phố Buôn Ma Thuột', 29),
	(324, 'Thị Xã Buôn Hồ', 29),
	(325, 'Huyện Cư Jút', 30),
	(326, 'Huyện Đăk Glong', 30),
	(327, 'Huyện Đắk Mil', 30),
	(328, 'Huyện Đắk R Lấp', 30),
	(329, 'Huyện Đắk Song', 30),
	(330, 'Huyện Krông Nô', 30),
	(331, 'Huyện Tuy Đức', 30),
	(332, 'Thành phố Gia Nghĩa', 30),
	(333, 'Huyện Điện Biên', 31),
	(334, 'Huyện Điện Biên Đông', 31),
	(335, 'Huyện Mường Ảng', 31),
	(336, 'Huyện Mường Chà', 31),
	(337, 'Huyện Mường Nhé', 31),
	(338, 'Huyện Nậm Pồ', 31),
	(339, 'Huyện Tủa Chùa', 31),
	(340, 'Huyện Tuần Giáo', 31),
	(341, 'Thành phố Điện Biên Phủ', 31),
	(342, 'Thị Xã Mường Lay', 31),
	(343, 'Huyện Chư Păh', 32),
	(344, 'Huyện Chư Prông', 32),
	(345, 'Huyện Chư Pưh', 32),
	(346, 'Huyện Chư Sê', 32),
	(347, 'Huyện Đăk Đoa', 32),
	(348, 'Huyện Đăk Pơ', 32),
	(349, 'Huyện Đức Cơ', 32),
	(350, 'Huyện Ia Grai', 32),
	(351, 'Huyện Ia Pa', 32),
	(352, 'Huyện KBang', 32),
	(353, 'Huyện Kông Chro', 32),
	(354, 'Huyện Krông Pa', 32),
	(355, 'Huyện Mang Yang', 32),
	(356, 'Huyện Phú Thiện', 32),
	(357, 'Thành phố Pleiku', 32),
	(358, 'Thị xã An Khê', 32),
	(359, 'Thị xã Ayun Pa', 32),
	(360, 'Huyện Bắc Mê', 33),
	(361, 'Huyện Bắc Quang', 33),
	(362, 'Huyện Đồng Văn', 33),
	(363, 'Huyện Hoàng Su Phì', 33),
	(364, 'Huyện Mèo Vạc', 33),
	(365, 'Huyện Quản Bạ', 33),
	(366, 'Huyện Quang Bình', 33),
	(367, 'Huyện Vị Xuyên', 33),
	(368, 'Huyện Xín Mần', 33),
	(369, 'Huyện Yên Minh', 33),
	(370, 'Thành phố Hà Giang', 33),
	(371, 'Huyện Bình Lục', 34),
	(372, 'Huyện Kim Bảng', 34),
	(373, 'Huyện Lý Nhân', 34),
	(374, 'Huyện Thanh Liêm', 34),
	(375, 'Thành phố Phủ Lý', 34),
	(376, 'Thị xã Duy Tiên', 34),
	(377, 'Huyện Cẩm Xuyên', 35),
	(378, 'Huyện Can Lộc', 35),
	(379, 'Huyện Đức Thọ', 35),
	(380, 'Huyện Hương Khê', 35),
	(381, 'Huyện Hương Sơn', 35),
	(382, 'Huyện Kỳ Anh', 35),
	(383, 'Huyện Lộc Hà', 35),
	(384, 'Huyện Nghi Xuân', 35),
	(385, 'Huyện Thạch Hà', 35),
	(386, 'Huyện Vũ Quang', 35),
	(387, 'Thành phố Hà Tĩnh', 35),
	(388, 'Thị xã Hồng Lĩnh', 35),
	(389, 'Thị xã Kỳ Anh', 35),
	(390, 'Huyện Bình Giang', 36),
	(391, 'Huyện Cẩm Giàng', 36),
	(392, 'Huyện Gia Lộc', 36),
	(393, 'Huyện Kim Thành', 36),
	(394, 'Huyện Nam Sách', 36),
	(395, 'Huyện Ninh Giang', 36),
	(396, 'Huyện Thanh Hà', 36),
	(397, 'Huyện Thanh Miện', 36),
	(398, 'Huyện Tứ Kỳ', 36),
	(399, 'Thành phố Chí Linh', 36),
	(400, 'Thành phố Hải Dương', 36),
	(401, 'Thị xã Kinh Môn', 36),
	(402, 'Huyện Cao Phong', 37),
	(403, 'Huyện Đà Bắc', 37),
	(404, 'Huyện Kim Bôi', 37),
	(405, 'Huyện Lạc Sơn', 37),
	(406, 'Huyện Lạc Thủy', 37),
	(407, 'Huyện Lương Sơn', 37),
	(408, 'Huyện Mai Châu', 37),
	(409, 'Huyện Tân Lạc', 37),
	(410, 'Huyện Yên Thủy', 37),
	(411, 'Thành phố Hòa Bình', 37),
	(412, 'Huyện Ân Thi', 38),
	(413, 'Huyện Khoái Châu', 38),
	(414, 'Huyện Kim Động', 38),
	(415, 'Huyện Phù Cừ', 38),
	(416, 'Huyện Tiên Lữ', 38),
	(417, 'Huyện Văn Giang', 38),
	(418, 'Huyện Văn Lâm', 38),
	(419, 'Huyện Yên Mỹ', 38),
	(420, 'Thành phố Hưng Yên', 38),
	(421, 'Thị xã Mỹ Hào', 38),
	(422, 'Huyện Cam Lâm', 39),
	(423, 'Huyện Diên Khánh', 39),
	(424, 'Huyện Khánh Sơn', 39),
	(425, 'Huyện Khánh Vĩnh', 39),
	(426, 'Huyện Trường Sa', 39),
	(427, 'Huyện Vạn Ninh', 39),
	(428, 'Thành phố Cam Ranh', 39),
	(429, 'Thành phố Nha Trang', 39),
	(430, 'Thị xã Ninh Hòa', 39),
	(431, 'Huyện Đắk Glei', 40),
	(432, 'Huyện Đắk Hà', 40),
	(433, 'Huyện Đắk Tô', 40),
	(434, 'Huyện Ia H Drai', 40),
	(435, 'Huyện Kon Plông', 40),
	(436, 'Huyện Kon Rẫy', 40),
	(437, 'Huyện Ngọc Hồi', 40),
	(438, 'Huyện Sa Thầy', 40),
	(439, 'Huyện Tu Mơ Rông', 40),
	(440, 'Thành phố Kon Tum', 40),
	(441, 'Huyện Mường Tè', 41),
	(442, 'Huyện Nậm Nhùn', 41),
	(443, 'Huyện Phong Thổ', 41),
	(444, 'Huyện Sìn Hồ', 41),
	(445, 'Huyện Tam Đường', 41),
	(446, 'Huyện Tân Uyên', 41),
	(447, 'Huyện Than Uyên', 41),
	(448, 'Thành phố Lai Châu', 41),
	(449, 'Huyện Bảo Lâm', 42),
	(450, 'Huyện Cát Tiên', 42),
	(451, 'Huyện Di Linh', 42),
	(452, 'Huyện Đạ Huoai', 42),
	(453, 'Huyện Đạ Tẻh', 42),
	(454, 'Huyện Đam Rông', 42),
	(455, 'Huyện Đơn Dương', 42),
	(456, 'Huyện Đức Trọng', 42),
	(457, 'Huyện Lạc Dương', 42),
	(458, 'Huyện Lâm Hà', 42),
	(459, 'Thành phố Bảo Lộc', 42),
	(460, 'Thành phố Đà Lạt', 42),
	(461, 'Huyện Bắc Sơn', 43),
	(462, 'Huyện Bình Gia', 43),
	(463, 'Huyện Cao Lộc', 43),
	(464, 'Huyện Chi Lăng', 43),
	(465, 'Huyện Đình Lập', 43),
	(466, 'Huyện Hữu Lũng', 43),
	(467, 'Huyện Lộc Bình', 43),
	(468, 'Huyện Tràng Định', 43),
	(469, 'Huyện Văn Lãng', 43),
	(470, 'Huyện Văn Quan', 43),
	(471, 'Thành phố Lạng Sơn', 43),
	(472, 'Huyện Bắc Hà', 44),
	(473, 'Huyện Bảo Thắng', 44),
	(474, 'Huyện Bảo Yên', 44),
	(475, 'Huyện Bát Xát', 44),
	(476, 'Huyện Mường Khương', 44),
	(477, 'Huyện Si Ma Cai', 44),
	(478, 'Huyện Văn Bàn', 44),
	(479, 'Thành phố Lào Cai', 44),
	(480, 'Thị xã Sa Pa', 44),
	(481, 'Huyện Giao Thủy', 45),
	(482, 'Huyện Hải Hậu', 45),
	(483, 'Huyện Mỹ Lộc', 45),
	(484, 'Huyện Nam Trực', 45),
	(485, 'Huyện Nghĩa Hưng', 45),
	(486, 'Huyện Trực Ninh', 45),
	(487, 'Huyện Vụ Bản', 45),
	(488, 'Huyện Xuân Trường', 45),
	(489, 'Huyện Ý Yên', 45),
	(490, 'Thành phố Nam Định', 45),
	(491, 'Huyện Anh Sơn', 46),
	(492, 'Huyện Con Cuông', 46),
	(493, 'Huyện Diễn Châu', 46),
	(494, 'Huyện Đô Lương', 46),
	(495, 'Huyện Hưng Nguyên', 46),
	(496, 'Huyện Kỳ Sơn', 46),
	(497, 'Huyện Nam Đàn', 46),
	(498, 'Huyện Nghi Lộc', 46),
	(499, 'Huyện Nghĩa Đàn', 46),
	(500, 'Huyện Quế Phong', 46),
	(501, 'Huyện Quỳ Châu', 46),
	(502, 'Huyện Quỳ Hợp', 46),
	(503, 'Huyện Quỳnh Lưu', 46),
	(504, 'Huyện Tân Kỳ', 46),
	(505, 'Huyện Thanh Chương', 46),
	(506, 'Huyện Tương Dương', 46),
	(507, 'Huyện Yên Thành', 46),
	(508, 'Thành phố Vinh', 46),
	(509, 'Thị xã Cửa Lò', 46),
	(510, 'Thị xã Hoàng Mai', 46),
	(511, 'Thị xã Thái Hoà', 46),
	(512, 'Huyện Gia Viễn', 47),
	(513, 'Huyện Hoa Lư', 47),
	(514, 'Huyện Kim Sơn', 47),
	(515, 'Huyện Nho Quan', 47),
	(516, 'Huyện Yên Khánh', 47),
	(517, 'Huyện Yên Mô', 47),
	(518, 'Thành phố Ninh Bình', 47),
	(519, 'Thành phố Tam Điệp', 47),
	(520, 'Huyện Bác Ái', 48),
	(521, 'Huyện Ninh Hải', 48),
	(522, 'Huyện Ninh Phước', 48),
	(523, 'Huyện Ninh Sơn', 48),
	(524, 'Huyện Thuận Bắc', 48),
	(525, 'Huyện Thuận Nam', 48),
	(526, 'Thành phố Phan Rang-Tháp Chàm', 48),
	(527, 'Huyện Cẩm Khê', 49),
	(528, 'Huyện Đoan Hùng', 49),
	(529, 'Huyện Hạ Hoà', 49),
	(530, 'Huyện Lâm Thao', 49),
	(531, 'Huyện Phù Ninh', 49),
	(532, 'Huyện Tam Nông', 49),
	(533, 'Huyện Tân Sơn', 49),
	(534, 'Huyện Thanh Ba', 49),
	(535, 'Huyện Thanh Sơn', 49),
	(536, 'Huyện Thanh Thuỷ', 49),
	(537, 'Huyện Yên Lập', 49),
	(538, 'Thành phố Việt Trì', 49),
	(539, 'Thị xã Phú Thọ', 49),
	(540, 'Huyện Đồng Xuân', 50),
	(541, 'Huyện Phú Hoà', 50),
	(542, 'Huyện Sơn Hòa', 50),
	(543, 'Huyện Sông Hinh', 50),
	(544, 'Huyện Tây Hoà', 50),
	(545, 'Huyện Tuy An', 50),
	(546, 'Thành phố Tuy Hoà', 50),
	(547, 'Thị xã Đông Hòa', 50),
	(548, 'Thị xã Sông Cầu', 50),
	(549, 'Huyện Bố Trạch', 51),
	(550, 'Huyện Lệ Thủy', 51),
	(551, 'Huyện Minh Hóa', 51),
	(552, 'Huyện Quảng Ninh', 51),
	(553, 'Huyện Quảng Trạch', 51),
	(554, 'Huyện Tuyên Hóa', 51),
	(555, 'Thành Phố Đồng Hới', 51),
	(556, 'Thị xã Ba Đồn', 51),
	(557, 'Huyện Bắc Trà My', 52),
	(558, 'Huyện Duy Xuyên', 52),
	(559, 'Huyện Đại Lộc', 52),
	(560, 'Huyện Đông Giang', 52),
	(561, 'Huyện Hiệp Đức', 52),
	(562, 'Huyện Nam Giang', 52),
	(563, 'Huyện Nam Trà My', 52),
	(564, 'Huyện Nông Sơn', 52),
	(565, 'Huyện Núi Thành', 52),
	(566, 'Huyện Phú Ninh', 52),
	(567, 'Huyện Phước Sơn', 52),
	(568, 'Huyện Quế Sơn', 52),
	(569, 'Huyện Tây Giang', 52),
	(570, 'Huyện Thăng Bình', 52),
	(571, 'Huyện Tiên Phước', 52),
	(572, 'Thành phố Hội An', 52),
	(573, 'Thành phố Tam Kỳ', 52),
	(574, 'Thị xã Điện Bàn', 52),
	(575, 'Huyện Ba Tơ', 53),
	(576, 'Huyện Bình Sơn', 53),
	(577, 'Huyện Minh Long', 53),
	(578, 'Huyện Mộ Đức', 53),
	(579, 'Huyện Nghĩa Hành', 53),
	(580, 'Huyện Sơn Hà', 53),
	(581, 'Huyện Sơn Tây', 53),
	(582, 'Huyện Sơn Tịnh', 53),
	(583, 'Huyện Trà Bồng', 53),
	(584, 'Huyện Tư Nghĩa', 53),
	(585, 'Thành phố Quảng Ngãi', 53),
	(586, 'Thị xã Đức Phổ', 53),
	(587, 'Huyện Ba Chẽ', 54),
	(588, 'Huyện Bình Liêu', 54),
	(589, 'Huyện Cô Tô', 54),
	(590, 'Huyện Đầm Hà', 54),
	(591, 'Huyện Hải Hà', 54),
	(592, 'Huyện Tiên Yên', 54),
	(593, 'Huyện Vân Đồn', 54),
	(594, 'Thành phố Cẩm Phả', 54),
	(595, 'Thành phố Hạ Long', 54),
	(596, 'Thành phố Móng Cái', 54),
	(597, 'Thành phố Uông Bí', 54),
	(598, 'Thị xã Đông Triều', 54),
	(599, 'Thị xã Quảng Yên', 54),
	(600, 'Huyện Cam Lộ', 55),
	(601, 'Huyện Đa Krông', 55),
	(602, 'Huyện Gio Linh', 55),
	(603, 'Huyện Hải Lăng', 55),
	(604, 'Huyện Hướng Hóa', 55),
	(605, 'Huyện Triệu Phong', 55),
	(606, 'Huyện Vĩnh Linh', 55),
	(607, 'Thành phố Đông Hà', 55),
	(608, 'Thị xã Quảng Trị', 55),
	(609, 'Huyện Bắc Yên', 56),
	(610, 'Huyện Mai Sơn', 56),
	(611, 'Huyện Mộc Châu', 56),
	(612, 'Huyện Mường La', 56),
	(613, 'Huyện Phù Yên', 56),
	(614, 'Huyện Quỳnh Nhai', 56),
	(615, 'Huyện Sông Mã', 56),
	(616, 'Huyện Sốp Cộp', 56),
	(617, 'Huyện Thuận Châu', 56),
	(618, 'Huyện Vân Hồ', 56),
	(619, 'Huyện Yên Châu', 56),
	(620, 'Thành phố Sơn La', 56),
	(621, 'Huyện Đông Hưng', 57),
	(622, 'Huyện Hưng Hà', 57),
	(623, 'Huyện Kiến Xương', 57),
	(624, 'Huyện Quỳnh Phụ', 57),
	(625, 'Huyện Thái Thụy', 57),
	(626, 'Huyện Tiền Hải', 57),
	(627, 'Huyện Vũ Thư', 57),
	(628, 'Thành phố Thái Bình', 57),
	(629, 'Huyện Đại Từ', 58),
	(630, 'Huyện Định Hóa', 58),
	(631, 'Huyện Đồng Hỷ', 58),
	(632, 'Huyện Phú Bình', 58),
	(633, 'Huyện Phú Lương', 58),
	(634, 'Huyện Võ Nhai', 58),
	(635, 'Thành phố Sông Công', 58),
	(636, 'Thành phố Thái Nguyên', 58),
	(637, 'Thị xã Phổ Yên', 58),
	(638, 'Huyện Bá Thước', 59),
	(639, 'Huyện Cẩm Thủy', 59),
	(640, 'Huyện Đông Sơn', 59),
	(641, 'Huyện Hà Trung', 59),
	(642, 'Huyện Hậu Lộc', 59),
	(643, 'Huyện Hoằng Hóa', 59),
	(644, 'Huyện Lang Chánh', 59),
	(645, 'Huyện Mường Lát', 59),
	(646, 'Huyện Nga Sơn', 59),
	(647, 'Huyện Ngọc Lặc', 59),
	(648, 'Huyện Như Thanh', 59),
	(649, 'Huyện Như Xuân', 59),
	(650, 'Huyện Nông Cống', 59),
	(651, 'Huyện Quan Hóa', 59),
	(652, 'Huyện Quan Sơn', 59),
	(653, 'Huyện Quảng Xương', 59),
	(654, 'Huyện Thạch Thành', 59),
	(655, 'Huyện Thiệu Hóa', 59),
	(656, 'Huyện Thọ Xuân', 59),
	(657, 'Huyện Thường Xuân', 59),
	(658, 'Huyện Triệu Sơn', 59),
	(659, 'Huyện Vĩnh Lộc', 59),
	(660, 'Huyện Yên Định', 59),
	(661, 'Thành phố Sầm Sơn', 59),
	(662, 'Thành phố Thanh Hóa', 59),
	(663, 'Thị xã Bỉm Sơn', 59),
	(664, 'Thị xã Nghi Sơn', 59),
	(665, 'Huyện A Lưới', 60),
	(666, 'Huyện Nam Đông', 60),
	(667, 'Huyện Phong Điền', 60),
	(668, 'Huyện Phú Lộc', 60),
	(669, 'Huyện Phú Vang', 60),
	(670, 'Huyện Quảng Điền', 60),
	(671, 'Thành phố Huế', 60),
	(672, 'Thị xã Hương Thủy', 60),
	(673, 'Thị xã Hương Trà', 60),
	(674, 'Huyện Chiêm Hóa', 61),
	(675, 'Huyện Hàm Yên', 61),
	(676, 'Huyện Lâm Bình', 61),
	(677, 'Huyện Na Hang', 61),
	(678, 'Huyện Sơn Dương', 61),
	(679, 'Huyện Yên Sơn', 61),
	(680, 'Thành phố Tuyên Quang', 61),
	(681, 'Huyện Bình Xuyên', 62),
	(682, 'Huyện Lập Thạch', 62),
	(683, 'Huyện Sông Lô', 62),
	(684, 'Huyện Tam Dương', 62),
	(685, 'Huyện Tam Đảo', 62),
	(686, 'Huyện Vĩnh Tường', 62),
	(687, 'Huyện Yên Lạc', 62),
	(688, 'Thành phố Phúc Yên', 62),
	(689, 'Thành phố Vĩnh Yên', 62),
	(690, 'Huyện Lục Yên', 63),
	(691, 'Huyện Mù Căng Chải', 63),
	(692, 'Huyện Trạm Tấu', 63),
	(693, 'Huyện Trấn Yên', 63),
	(694, 'Huyện Văn Chấn', 63),
	(695, 'Huyện Văn Yên', 63),
	(696, 'Huyện Yên Bình', 63),
	(697, 'Thành phố Yên Bái', 63),
	(698, 'Thị xã Nghĩa Lộ', 63),
	(699, 'Huyện Côn Đảo', 2),
	(700, 'Huyện Hoà Thành', 16),
	(701, 'Thi Xã Từ Sơn', 25),
	(702, 'Huyện Thông Nông', 28),
	(703, 'Huyện Trà Lĩnh', 28),
	(704, 'Huyện Phục Hòa', 28),
	(705, 'Huyện Quảng Uyên', 28),
	(706, 'Huyện Buôn Ðôn', 29),
	(707, 'Thị Xã Gia Nghĩa', 30),
	(708, 'Huyện Hồng Ngự', 10),
	(709, 'Huyện Duy Tiên', 34),
	(710, 'Huyện Kinh Môn', 36),
	(711, 'Huyện Long Mỹ', 11),
	(712, 'Huyện Kỳ Sơn', 37),
	(713, 'Huyện Ia HDrai', 40),
	(714, 'Huyện Sa Pa', 44),
	(715, 'Huyện Đông Hòa', 50),
	(716, 'Huyện Lý Sơn', 53),
	(717, 'Huyện Đức Phổ', 53),
	(718, 'Huyện Tây Trà', 53),
	(719, 'Huyện Hoành Bồ', 54),
	(720, 'Huyện Đakrông', 55),
	(721, 'Huyện Tĩnh Gia', 59),
	(722, 'Huyện Cai Lậy', 17),
	(723, 'Huyện Cao Lãnh', 10),
	(724, 'Thành Phố Thủ Đức', 12)
    """)
    pass


def downgrade():
    op.drop_table('address_level_2')
    pass
