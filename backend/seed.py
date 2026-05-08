"""Seed script to insert sample data for local testing.

Run with: python seed.py (from backend directory)
           or via docker-compose command.

This script is idempotent: it checks primary keys before inserting, and updates existing records.
"""
import asyncio
import os
from typing import List, Dict

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.paper import Paper
from app.models.summary import Summary


USERS: List[Dict] = [
    # ROOT user — password: "123456"
    {"id": 1, "email": "admin@example.com", "full_name": "Quản trị viên Cấp cao", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "root"},
    # ADMIN users — password: "123456"
    {"id": 2, "email": "manager1@example.com", "full_name": "Quản lý Dự án", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "admin"},
    {"id": 3, "email": "manager2@example.com", "full_name": "Quản lý Nội dung", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "admin"},
    # Regular users — password: "123456"
    {"id": 4, "email": "user1@example.com", "full_name": "Người dùng số 1", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 5, "email": "user2@example.com", "full_name": "Người dùng số 2", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 6, "email": "user3@example.com", "full_name": "Người dùng số 3", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 7, "email": "user4@example.com", "full_name": "Người dùng số 4", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 8, "email": "user5@example.com", "full_name": "Người dùng số 5", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 9, "email": "user6@example.com", "full_name": "Người dùng số 6", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 10, "email": "user7@example.com", "full_name": "Người dùng số 7", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 11, "email": "user8@example.com", "full_name": "Người dùng số 8", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 12, "email": "user9@example.com", "full_name": "Người dùng số 9", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 13, "email": "user10@example.com", "full_name": "Người dùng số 10", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 14, "email": "user11@example.com", "full_name": "Người dùng số 11", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 15, "email": "user12@example.com", "full_name": "Người dùng số 12", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
]

PAPERS: List[Dict] = [
    # Computer Science & AI
    {"id": 1, "user_id": 2, "title": "Nghiên cứu về Học máy", "content": "Học máy là tập hợp thuật toán cho phép hệ thống học từ dữ liệu mà không cần lập trình rõ ràng.", "file_path": None},
    {"id": 2, "user_id": 2, "title": "Ứng dụng NLP trong y tế", "content": "NLP giúp phân tích hồ sơ bệnh án, trích xuất thông tin lâm sàng và hỗ trợ chẩn đoán.", "file_path": None},
    {"id": 3, "user_id": 3, "title": "Mạng nơ-ron sâu", "content": "Mạng sâu gồm nhiều lớp ẩn để học biểu diễn phức tạp của hình ảnh, âm thanh và văn bản.", "file_path": None},
    {"id": 4, "user_id": 4, "title": "Blockchain cơ bản", "content": "Nguyên lý chuỗi khối, smart contracts và bằng chứng công việc trong mạng phi tập trung.", "file_path": None},
    {"id": 5, "user_id": 5, "title": "Điện toán đám mây & Serverless", "content": "Sự tiến hóa của kiến trúc phần mềm sang mô hình Serverless giúp tối ưu chi phí và tự động mở rộng.", "file_path": None},
    {"id": 6, "user_id": 6, "title": "Bảo mật Zero-Trust", "content": "Mô hình bảo mật không tin cậy bất kỳ ai kể cả trong mạng nội bộ, yêu cầu xác thực liên tục.", "file_path": None},
    
    # Y sinh & Sức khỏe (Biology & Medicine)
    {"id": 7, "user_id": 7, "title": "Công nghệ mRNA trong Vaccine", "content": "Cơ chế hoạt động của vaccine mRNA trong việc kích hoạt hệ miễn dịch chống lại virus SARS-CoV-2.", "file_path": None},
    {"id": 8, "user_id": 8, "title": "Chỉnh sửa gen CRISPR-Cas9", "content": "Tiềm năng của CRISPR trong việc điều trị các bệnh di truyền và những thách thức đạo đức.", "file_path": None},
    {"id": 9, "user_id": 9, "title": "Phân tích hệ vi sinh vật đường ruột", "content": "Tác động của hệ vi sinh vật đường ruột đến sức khỏe tâm thần, tiêu hóa và bệnh lý béo phì.", "file_path": None},
    {"id": 10, "user_id": 10, "title": "Ung thư học phân tử", "content": "Khám phá các đột biến gen gây ung thư và phương pháp điều trị đích (targeted therapy).", "file_path": None},
    {"id": 11, "user_id": 11, "title": "Khoa học Giấc ngủ", "content": "Vai trò của giấc ngủ REM và Non-REM trong việc củng cố trí nhớ và phục hồi thể chất.", "file_path": None},

    # Kinh tế & Tài chính (Economics & Finance)
    {"id": 12, "user_id": 12, "title": "Tác động của Lạm phát toàn cầu", "content": "Phân tích nguyên nhân lạm phát sau đại dịch và các chính sách thắt chặt tiền tệ của FED.", "file_path": None},
    {"id": 13, "user_id": 13, "title": "Tiền mã hóa và DeFi", "content": "Sự trỗi dậy của tài chính phi tập trung (DeFi) và rủi ro bong bóng trong thị trường Crypto.", "file_path": None},
    {"id": 14, "user_id": 14, "title": "Kinh tế tuần hoàn", "content": "Mô hình phát triển bền vững, giảm thiểu rác thải thông qua tái chế và tối ưu hóa tài nguyên.", "file_path": None},
    {"id": 15, "user_id": 15, "title": "Đầu tư giá trị & Phân tích cơ bản", "content": "Phương pháp định giá doanh nghiệp dựa trên dòng tiền tương lai và chỉ số tài chính.", "file_path": None},
    {"id": 16, "user_id": 2, "title": "Hành vi người tiêu dùng Gen Z", "content": "Sự dịch chuyển thói quen mua sắm trực tuyến, sự ưa chuộng tính bền vững và xu hướng TikTok.", "file_path": None},

    # Lịch sử & Văn hóa (History & Culture)
    {"id": 17, "user_id": 3, "title": "Sự sụp đổ của Đế chế La Mã", "content": "Nguyên nhân chính trị, kinh tế và quân sự dẫn đến sự suy tàn của một đế chế vĩ đại.", "file_path": None},
    {"id": 18, "user_id": 4, "title": "Cách mạng Công nghiệp lần thứ hai", "content": "Sự phát triển của điện lực, hóa học và sản xuất hàng loạt vào cuối thế kỷ 19.", "file_path": None},
    {"id": 19, "user_id": 5, "title": "Chiến tranh Lạnh và Cuộc chạy đua Không gian", "content": "Sự ganh đua giữa Mỹ và Liên Xô thúc đẩy tiến bộ công nghệ nhảy vọt trong thế kỷ 20.", "file_path": None},
    {"id": 20, "user_id": 6, "title": "Văn hóa Đại chúng và Toàn cầu hóa", "content": "Sự bành trướng của âm nhạc, phim ảnh Hollywood và K-Pop tới văn hóa bản địa.", "file_path": None},
    {"id": 21, "user_id": 7, "title": "Phục hưng Ý (Renaissance)", "content": "Sự trỗi dậy của nghệ thuật, văn học và khoa học ở châu Âu sau Đêm trường Trung cổ.", "file_path": None},

    # Kỹ thuật & Môi trường (Engineering & Environment)
    {"id": 22, "user_id": 8, "title": "Năng lượng tái tạo: Lưu trữ điện năng", "content": "Công nghệ pin Lithium-ion, Solid-state battery và giải pháp lưu trữ năng lượng mặt trời.", "file_path": None},
    {"id": 23, "user_id": 9, "title": "Khai phá không gian & Sao Hỏa", "content": "Tên lửa tái sử dụng và lộ trình đưa con người lên định cư Sao Hỏa của các tập đoàn tư nhân.", "file_path": None},
    {"id": 24, "user_id": 10, "title": "Tác động của biến đổi khí hậu", "content": "Gia tăng mực nước biển đe dọa trực tiếp đến sinh kế của hàng triệu người tại các vùng ven biển.", "file_path": None},
    {"id": 25, "user_id": 11, "title": "Kiến trúc xanh & Vật liệu thân thiện", "content": "Ứng dụng vật liệu tái chế và thiết kế tối ưu ánh sáng tự nhiên trong các tòa nhà cao tầng.", "file_path": None},
    {"id": 26, "user_id": 12, "title": "Xe điện và Hạ tầng trạm sạc", "content": "Những thách thức trong việc phủ sóng hạ tầng sạc nhanh để thúc đẩy kỷ nguyên xe điện.", "file_path": None},

    # Giáo dục, Xã hội & Luật (Education, Society & Law)
    {"id": 27, "user_id": 13, "title": "Giáo dục trực tuyến thời kỳ hậu COVID", "content": "Sự chuyển dịch học tập, ưu và nhược điểm của E-learning đối với sự phát triển kỹ năng xã hội.", "file_path": None},
    {"id": 28, "user_id": 14, "title": "Bản quyền trong thời đại AI tạo sinh", "content": "Các thách thức pháp lý khi AI học tập dựa trên tranh ảnh và văn bản có bản quyền của nghệ sĩ.", "file_path": None},
    {"id": 29, "user_id": 15, "title": "Tác động của mạng xã hội tới giới trẻ", "content": "Hiệu ứng FOMO, trầm cảm và suy giảm khả năng tập trung do thuật toán gây nghiện.", "file_path": None},
    {"id": 30, "user_id": 2, "title": "Bất bình đẳng thu nhập", "content": "Hố sâu ngăn cách giàu nghèo ngày càng gia tăng và tác động tiêu cực đến sự ổn định xã hội.", "file_path": None},
    
    # Tâm lý học & Triết học (Psychology & Philosophy)
    {"id": 31, "user_id": 3, "title": "Liệu pháp nhận thức hành vi (CBT)", "content": "Cách CBT giúp bệnh nhân thay đổi suy nghĩ tiêu cực và khắc phục chứng rối loạn lo âu.", "file_path": None},
    {"id": 32, "user_id": 4, "title": "Nghịch lý của sự lựa chọn", "content": "Vì sao quá nhiều lựa chọn lại khiến con người căng thẳng và khó thỏa mãn hơn.", "file_path": None},
    {"id": 33, "user_id": 5, "title": "Trí tuệ cảm xúc (EQ) trong lãnh đạo", "content": "Tại sao EQ đóng vai trò quan trọng hơn IQ trong việc quản lý và truyền cảm hứng cho đội ngũ.", "file_path": None},
    {"id": 34, "user_id": 6, "title": "Thuyết vị lợi (Utilitarianism)", "content": "Triết lý hành động mang lại hạnh phúc lớn nhất cho số đông lớn nhất và các tranh cãi đạo đức.", "file_path": None},
    
    # Khoa học tự nhiên (Natural Sciences)
    {"id": 35, "user_id": 7, "title": "Điện toán Lượng tử", "content": "Nguyên lý Chồng chập và Vướng mắc lượng tử hứa hẹn thay đổi sức mạnh tính toán máy tính.", "file_path": None},
    {"id": 36, "user_id": 8, "title": "Lỗ đen và Thuyết tương đối rộng", "content": "Sự bẻ cong không thời gian và những hiểu biết mới nhất về sự hình thành của siêu lỗ đen.", "file_path": None},
    {"id": 37, "user_id": 9, "title": "Sự tuyệt chủng kỷ Creta-Paleogen", "content": "Giả thuyết thiên thạch và quá trình diệt vong của loài khủng long cách đây 66 triệu năm.", "file_path": None},
    {"id": 38, "user_id": 10, "title": "Hạt Higgs Boson", "content": "Khám phá về Hạt của Chúa và vai trò của nó trong việc tạo ra khối lượng cho các hạt cơ bản.", "file_path": None},
    {"id": 39, "user_id": 11, "title": "Biến đổi gen ở cây trồng", "content": "Sử dụng công nghệ sinh học tạo ra giống cây chịu hạn, kháng sâu bệnh giải quyết nạn đói.", "file_path": None},
    {"id": 40, "user_id": 12, "title": "Thuyết Đa vũ trụ (Multiverse)", "content": "Giả thuyết về sự tồn tại của vô số vũ trụ song song và giới hạn của vật lý lý thuyết.", "file_path": None},
]

SUMMARIES: List[Dict] = [
    # CS & AI
    {"id": 1, "paper_id": 1, "type": "short", "content": "Tóm tắt: Học máy cho phép tạo mô hình dự đoán từ dữ liệu quá khứ."},
    {"id": 2, "paper_id": 2, "type": "short", "content": "Tóm tắt: NLP hỗ trợ trích xuất thông tin y tế tự động từ hồ sơ lâm sàng."},
    {"id": 3, "paper_id": 3, "type": "short", "content": "Tóm tắt: Deep Learning sử dụng mạng nhiều lớp cho dữ liệu phi cấu trúc."},
    {"id": 4, "paper_id": 4, "type": "short", "content": "Tóm tắt: Blockchain đảm bảo tính toàn vẹn và minh bạch dữ liệu nhờ mạng phi tập trung."},
    {"id": 5, "paper_id": 5, "type": "short", "content": "Tóm tắt: Serverless loại bỏ gánh nặng quản lý hạ tầng, tính tiền theo thời gian chạy."},
    {"id": 6, "paper_id": 6, "type": "short", "content": "Tóm tắt: Zero-Trust giả định mọi kết nối đều có nguy cơ, yêu cầu xác thực liên tục."},
    
    # Y sinh
    {"id": 7, "paper_id": 7, "type": "short", "content": "Tóm tắt: mRNA kích hoạt miễn dịch tế bào nhanh và an toàn hơn vaccine truyền thống."},
    {"id": 8, "paper_id": 8, "type": "short", "content": "Tóm tắt: CRISPR giúp cắt dán gen, mở cơ hội chữa bệnh di truyền nhưng vướng rào cản đạo đức."},
    {"id": 9, "paper_id": 9, "type": "short", "content": "Tóm tắt: Hệ vi sinh đường ruột đóng vai trò như một bộ não thứ hai điều hòa cơ thể."},
    {"id": 10, "paper_id": 10, "type": "short", "content": "Tóm tắt: Phân tích gen ung thư giúp điều trị đích hiệu quả và giảm tác dụng phụ."},
    {"id": 11, "paper_id": 11, "type": "short", "content": "Tóm tắt: Ngủ không đủ giấc dẫn đến suy giảm nhận thức và tăng rủi ro bệnh chuyển hóa."},

    # Kinh tế
    {"id": 12, "paper_id": 12, "type": "short", "content": "Tóm tắt: Lạm phát gia tăng do đứt gãy chuỗi cung ứng và chính sách bơm tiền quá mức."},
    {"id": 13, "paper_id": 13, "type": "short", "content": "Tóm tắt: DeFi loại bỏ ngân hàng trung gian nhưng tiềm ẩn nguy cơ hack smart contract."},
    {"id": 14, "paper_id": 14, "type": "short", "content": "Tóm tắt: Kinh tế tuần hoàn biến rác thải thành nguyên liệu đầu vào cho chu trình mới."},
    {"id": 15, "paper_id": 15, "type": "short", "content": "Tóm tắt: Đầu tư giá trị tập trung vào nội tại doanh nghiệp thay vì biến động thị trường."},
    {"id": 16, "paper_id": 16, "type": "short", "content": "Tóm tắt: Gen Z ưu tiên các thương hiệu xanh và mua sắm chịu ảnh hưởng mạnh bởi MXH."},

    # Lịch sử
    {"id": 17, "paper_id": 17, "type": "short", "content": "Tóm tắt: La Mã suy tàn do khủng hoảng kinh tế, tham nhũng và áp lực từ ngoại bang."},
    {"id": 18, "paper_id": 18, "type": "short", "content": "Tóm tắt: Động cơ đốt trong và điện khí hóa đã thay đổi hoàn toàn cục diện sản xuất kỷ 19."},
    {"id": 19, "paper_id": 19, "type": "short", "content": "Tóm tắt: Chạy đua không gian là thành tựu vĩ đại được thúc đẩy bởi đối đầu chính trị Mỹ-Xô."},
    {"id": 20, "paper_id": 20, "type": "short", "content": "Tóm tắt: Toàn cầu hóa giúp văn hóa đại chúng lan tỏa nhưng đe dọa bản sắc địa phương."},
    {"id": 21, "paper_id": 21, "type": "short", "content": "Tóm tắt: Phục hưng khơi mào cho tư duy nhân văn và sự bùng nổ của nghệ thuật châu Âu."},

    # Kỹ thuật
    {"id": 22, "paper_id": 22, "type": "short", "content": "Tóm tắt: Lưu trữ điện năng quy mô lớn là chìa khóa để chuyển đổi 100% năng lượng sạch."},
    {"id": 23, "paper_id": 23, "type": "short", "content": "Tóm tắt: Tên lửa tái sử dụng giảm thiểu 90% chi phí vận chuyển hàng hóa lên quỹ đạo."},
    {"id": 24, "paper_id": 24, "type": "short", "content": "Tóm tắt: Mực nước biển dâng do băng tan đe dọa sinh kế hàng triệu người vùng ven biển."},
    {"id": 25, "paper_id": 25, "type": "short", "content": "Tóm tắt: Tòa nhà xanh giúp giảm khí nhà kính và tiết kiệm 30-50% điện năng."},
    {"id": 26, "paper_id": 26, "type": "short", "content": "Tóm tắt: Thiếu trạm sạc là rào cản lớn nhất ngăn cản sự phổ cập nhanh chóng của xe điện."},

    # Xã hội & Luật
    {"id": 27, "paper_id": 27, "type": "short", "content": "Tóm tắt: EdTech lên ngôi, nhưng thiếu tương tác xã hội là điểm yếu của học online."},
    {"id": 28, "paper_id": 28, "type": "short", "content": "Tóm tắt: Luật bản quyền hiện hành gặp lúng túng trước dữ liệu huấn luyện của các mô hình AI."},
    {"id": 29, "paper_id": 29, "type": "short", "content": "Tóm tắt: Thuật toán gây nghiện của MXH làm tăng tỷ lệ trầm cảm và thiếu tập trung ở thanh thiếu niên."},
    {"id": 30, "paper_id": 30, "type": "short", "content": "Tóm tắt: Bất bình đẳng thu nhập tạo ra phân hóa giai cấp sâu sắc và bất ổn chính trị."},

    # Tâm lý học
    {"id": 31, "paper_id": 31, "type": "short", "content": "Tóm tắt: CBT hiệu quả cao nhờ tập trung sửa đổi các niềm tin cốt lõi sai lệch."},
    {"id": 32, "paper_id": 32, "type": "short", "content": "Tóm tắt: Ít lựa chọn giúp con người ra quyết định nhanh và cảm thấy hạnh phúc hơn."},
    {"id": 33, "paper_id": 33, "type": "short", "content": "Tóm tắt: EQ cao giúp lãnh đạo thấu cảm và giải quyết xung đột nội bộ tốt hơn IQ."},
    {"id": 34, "paper_id": 34, "type": "short", "content": "Tóm tắt: Thuyết vị lợi đôi khi phải hi sinh thiểu số để bảo vệ lợi ích của đa số."},

    # Khoa học tự nhiên
    {"id": 35, "paper_id": 35, "type": "short", "content": "Tóm tắt: Máy tính lượng tử sẽ bẻ khóa mọi hệ thống mã hóa mật mã học truyền thống."},
    {"id": 36, "paper_id": 36, "type": "short", "content": "Tóm tắt: Lỗ đen có lực hấp dẫn mạnh đến mức ánh sáng cũng không thể thoát ra."},
    {"id": 37, "paper_id": 37, "type": "short", "content": "Tóm tắt: Thiên thạch va chạm gây ra biến đổi khí hậu đột ngột, xóa sổ loài khủng long."},
    {"id": 38, "paper_id": 38, "type": "short", "content": "Tóm tắt: Hạt Higgs giúp hoàn thiện Mô hình Chuẩn của vật lý hạt vi mô."},
    {"id": 39, "paper_id": 39, "type": "short", "content": "Tóm tắt: Cây trồng GMO cho năng suất cao nhưng đối mặt với sự e ngại của người tiêu dùng."},
    {"id": 40, "paper_id": 40, "type": "short", "content": "Tóm tắt: Đa vũ trụ lý giải sự tinh chỉnh hoàn hảo của vật lý để có sự sống."},
]


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        # Insert users
        for u in USERS:
            existing = await session.get(User, u["id"])
            if not existing:
                session.add(User(**u))
            else:
                for key, value in u.items():
                    setattr(existing, key, value)

        await session.commit()

        # Insert papers
        for p in PAPERS:
            existing = await session.get(Paper, p["id"])
            if not existing:
                session.add(Paper(**p))
            else:
                for key, value in p.items():
                    setattr(existing, key, value)

        await session.commit()

        # Insert summaries
        for s in SUMMARIES:
            existing = await session.get(Summary, s["id"])
            if not existing:
                session.add(Summary(**s))
            else:
                for key, value in s.items():
                    setattr(existing, key, value)

        await session.commit()


def main() -> None:
    # Only seed when explicitly enabled via ENV variable. Default: false.
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB != true — skipping seeding.")
        return
    asyncio.run(seed())


if __name__ == "__main__":
    main()
