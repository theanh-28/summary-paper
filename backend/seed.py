"""Seed script to insert sample data for local testing.

Run with: python seed.py (from backend directory)
           or via docker-compose command.

This script is idempotent: it checks primary keys before inserting.
"""
import asyncio
import os
from typing import List, Dict

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.paper import Paper
from app.models.summary import Summary


USERS: List[Dict] = [
    # Admin user — password: "123456"
    {"id": 1, "email": "admin@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "admin"},
    # Regular users — password: "123456"
    {"id": 2, "email": "user@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 3, "email": "user2@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 4, "email": "user3@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 5, "email": "user4@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 6, "email": "user6@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 7, "email": "user7@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 8, "email": "user8@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 9, "email": "user9@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 10, "email": "user10@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 11, "email": "user11@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 12, "email": "user12@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 13, "email": "user13@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 14, "email": "user14@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
    {"id": 15, "email": "user15@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo=", "role": "user"},
]

PAPERS: List[Dict] = [
    {"id": 2, "user_id": 2, "title": "Nghiên cứu về Học máy", "content": "Nội dung ví dụ: Học máy là tập hợp thuật toán cho phép hệ thống học từ dữ liệu.", "file_path": None},
    {"id": 3, "user_id": 2, "title": "Ứng dụng NLP trong y tế", "content": "Nội dung ví dụ: NLP giúp phân tích hồ sơ bệnh án và trích xuất thông tin.", "file_path": None},
    {"id": 4, "user_id": 3, "title": "Mạng nơ-ron sâu", "content": "Nội dung ví dụ: Mạng sâu gồm nhiều lớp ẩn để học biểu diễn phức tạp.", "file_path": None},
    {"id": 5, "user_id": 3, "title": "Thị giác máy tính", "content": "Nội dung ví dụ: Thị giác máy tính xử lý hình ảnh để nhận diện đối tượng.", "file_path": "uploads/cv_paper.pdf"},
    {"id": 6, "user_id": 4, "title": "Hệ khuyến nghị", "content": "Nội dung ví dụ: Hệ khuyến nghị đề xuất sản phẩm dựa trên lịch sử người dùng.", "file_path": None},
    {"id": 7, "user_id": 4, "title": "Robotics và điều khiển", "content": "Nội dung ví dụ: Robotics kết hợp phần mềm và phần cứng để tự động hóa nhiệm vụ.", "file_path": None},
    {"id": 8, "user_id": 5, "title": "An ninh mạng cơ bản", "content": "Nội dung ví dụ: Tấn công và phòng thủ trong an ninh mạng.", "file_path": None},
    {"id": 9, "user_id": 5, "title": "Khoa học dữ liệu cho doanh nghiệp", "content": "Nội dung ví dụ: Phân tích dữ liệu giúp ra quyết định kinh doanh.", "file_path": None},
    {"id": 10, "user_id": 1, "title": "Tổng quan về AI đạo đức", "content": "Nội dung ví dụ: Vấn đề đạo đức khi triển khai AI trong đời sống.", "file_path": None},
    {"id": 11, "user_id": 2, "title": "Tri thức biểu diễn và Semantic Web", "content": "Nội dung ví dụ: Semantic Web giúp kết nối dữ liệu ngữ nghĩa.", "file_path": None},
    {"id": 12, "user_id": 3, "title": "Tối ưu hóa và thuật toán", "content": "Nội dung ví dụ: Các thuật toán tối ưu hóa giúp tìm nghiệm tốt cho bài toán.", "file_path": None},
    {"id": 13, "user_id": 6, "title": "Mô hình đồ thị và ứng dụng", "content": "Nội dung: Ứng dụng đồ thị trong mạng xã hội và tìm đường ngắn nhất.", "file_path": None},
    {"id": 14, "user_id": 6, "title": "Xử lý tín hiệu số", "content": "Nội dung: Các phương pháp lọc và biến đổi tín hiệu.", "file_path": None},
    {"id": 15, "user_id": 7, "title": "Hệ phân tán và consistency", "content": "Nội dung: CAP theorem và các mô hình consistency.", "file_path": None},
    {"id": 16, "user_id": 7, "title": "Cơ sở dữ liệu NoSQL", "content": "Nội dung: Kiến trúc và trade-offs giữa SQL và NoSQL.", "file_path": None},
    {"id": 17, "user_id": 8, "title": "Blockchain cơ bản", "content": "Nội dung: Nguyên lý chuỗi khối và bằng chứng công việc.", "file_path": None},
    {"id": 18, "user_id": 8, "title": "Hệ thống khuyến nghị nâng cao", "content": "Nội dung: Collaborative filtering và matrix factorization.", "file_path": None},
    {"id": 19, "user_id": 9, "title": "Thị trường chứng khoán và ML", "content": "Nội dung: Ứng dụng học máy trong dự đoán thị trường tài chính.", "file_path": None},
    {"id": 20, "user_id": 9, "title": "Xử lý ảnh y tế", "content": "Nội dung: Mạng CNN cho chẩn đoán hình ảnh y tế.", "file_path": None},
    {"id": 21, "user_id": 10, "title": "Tối ưu hóa hyperparameter", "content": "Nội dung: Grid search, random search, Bayesian optimization.", "file_path": None},
    {"id": 22, "user_id": 10, "title": "Học tăng cường cơ bản", "content": "Nội dung: Mô hình agent, reward, môi trường.", "file_path": None},
    {"id": 23, "user_id": 11, "title": "Tri thức nhân tạo thông minh", "content": "Nội dung: Hệ expert systems và luật sản xuất.", "file_path": None},
    {"id": 24, "user_id": 11, "title": "Kiến trúc microservices", "content": "Nội dung: Thiết kế services, giao tiếp và triển khai.", "file_path": None},
    {"id": 25, "user_id": 12, "title": "Phân tích ngôn ngữ cảm xúc", "content": "Nội dung: Sentiment analysis trên dữ liệu mạng xã hội.", "file_path": None},
    {"id": 26, "user_id": 12, "title": "Compression algorithms", "content": "Nội dung: LZW, Huffman và các thuật toán nén dữ liệu.", "file_path": None},
    {"id": 27, "user_id": 13, "title": "Hệ thống thời gian thực", "content": "Nội dung: Kiến trúc xử lý stream và latency thấp.", "file_path": None},
    {"id": 28, "user_id": 13, "title": "An toàn ứng dụng web", "content": "Nội dung: OWASP top 10 và phòng chống XSS/CSRF.", "file_path": None},
    {"id": 29, "user_id": 14, "title": "Tiếng nói và nhận dạng giọng nói", "content": "Nội dung: Speech-to-text và mô hình acoustic.", "file_path": None},
    {"id": 30, "user_id": 14, "title": "Trí tuệ nhân tạo explainable", "content": "Nội dung: Lý giải quyết định mô hình ML (XAI).", "file_path": None},
    {"id": 31, "user_id": 15, "title": "IoT và edge computing", "content": "Nội dung: Xử lý tại edge cho thiết bị IoT.", "file_path": None},
    {"id": 32, "user_id": 15, "title": "Testing tự động cho ML", "content": "Nội dung: Validation pipelines và data drift detection.", "file_path": None},
]

SUMMARIES: List[Dict] = [
    {"id": 2, "paper_id": 2, "type": "short", "content": "Tóm tắt: Học máy học từ dữ liệu để tạo mô hình dự đoán."},
    {"id": 3, "paper_id": 3, "type": "short", "content": "Tóm tắt: NLP hỗ trợ xử lý ngôn ngữ tự nhiên trong y tế."},
    {"id": 4, "paper_id": 4, "type": "short", "content": "Tóm tắt: Mạng nơ-ron sâu học biểu diễn dữ liệu phức tạp."},
    {"id": 5, "paper_id": 5, "type": "short", "content": "Tóm tắt: Thị giác máy tính nhận diện đối tượng trong ảnh."},
    {"id": 6, "paper_id": 6, "type": "short", "content": "Tóm tắt: Hệ khuyến nghị đề xuất dựa trên lịch sử và tương tự."},
    {"id": 7, "paper_id": 7, "type": "short", "content": "Tóm tắt: Robotics kết hợp phần mềm và phần cứng để tự động hóa."},
    {"id": 8, "paper_id": 8, "type": "short", "content": "Tóm tắt: An ninh mạng liên quan tới phòng thủ và tấn công."},
    {"id": 9, "paper_id": 9, "type": "short", "content": "Tóm tắt: Khoa học dữ liệu hỗ trợ quyết định doanh nghiệp."},
    {"id": 10, "paper_id": 10, "type": "short", "content": "Tóm tắt: Bàn về đạo đức khi triển khai hệ thống AI."},
    {"id": 11, "paper_id": 11, "type": "short", "content": "Tóm tắt: Semantic Web cho phép kết nối dữ liệu có ý nghĩa."},
    {"id": 12, "paper_id": 12, "type": "short", "content": "Tóm tắt: Thuật toán tối ưu hóa tìm nghiệm tốt cho bài toán."},
    {"id": 13, "paper_id": 13, "type": "short", "content": "Tóm tắt: Mô hình đồ thị hỗ trợ phân tích mạng xã hội và tìm đường ngắn."},
    {"id": 14, "paper_id": 14, "type": "short", "content": "Tóm tắt: Kỹ thuật xử lý tín hiệu để lọc và biến đổi dữ liệu thời gian."},
    {"id": 15, "paper_id": 15, "type": "short", "content": "Tóm tắt: Hệ phân tán đối chiếu CAP và trade-offs consistency."},
    {"id": 16, "paper_id": 16, "type": "short", "content": "Tóm tắt: NoSQL cung cấp khả năng mở rộng ở chi phí nhất định so với SQL."},
    {"id": 17, "paper_id": 17, "type": "short", "content": "Tóm tắt: Blockchain là sổ cái phân tán với cơ chế đồng thuận."},
    {"id": 18, "paper_id": 18, "type": "short", "content": "Tóm tắt: Các thuật toán recommendation bao gồm collaborative filtering."},
    {"id": 19, "paper_id": 19, "type": "short", "content": "Tóm tắt: ML được dùng trong phân tích và dự đoán biến động tài chính."},
    {"id": 20, "paper_id": 20, "type": "short", "content": "Tóm tắt: CNN ứng dụng trong phân tích ảnh y tế để hỗ trợ chẩn đoán."},
    {"id": 21, "paper_id": 21, "type": "short", "content": "Tóm tắt: Các phương pháp tối ưu hóa hyperparameter cải thiện hiệu năng mô hình."},
    {"id": 22, "paper_id": 22, "type": "short", "content": "Tóm tắt: Học tăng cường đào tạo agent qua tương tác và reward."},
    {"id": 23, "paper_id": 23, "type": "short", "content": "Tóm tắt: Expert systems sử dụng luật để mô phỏng tri thức chuyên gia."},
    {"id": 24, "paper_id": 24, "type": "short", "content": "Tóm tắt: Microservices tách ứng dụng thành services độc lập dễ vận hành."},
    {"id": 25, "paper_id": 25, "type": "short", "content": "Tóm tắt: Sentiment analysis phân tích cảm xúc từ dữ liệu text."},
    {"id": 26, "paper_id": 26, "type": "short", "content": "Tóm tắt: Thuật toán nén dữ liệu giúp giảm kích thước lưu trữ và băng thông."},
    {"id": 27, "paper_id": 27, "type": "short", "content": "Tóm tắt: Hệ thống thời gian thực xử lý stream để phản hồi nhanh."},
    {"id": 28, "paper_id": 28, "type": "short", "content": "Tóm tắt: Bảo mật web tập trung vào OWASP top 10 và biện pháp phòng vệ."},
    {"id": 29, "paper_id": 29, "type": "short", "content": "Tóm tắt: Nhận dạng giọng nói chuyển speech sang text bằng mô hình acoustic."},
    {"id": 30, "paper_id": 30, "type": "short", "content": "Tóm tắt: XAI giúp giải thích quyết định của mô hình ML cho người dùng."},
    {"id": 31, "paper_id": 31, "type": "short", "content": "Tóm tắt: Edge computing xử lý dữ liệu gần nguồn để giảm latency."},
    {"id": 32, "paper_id": 32, "type": "short", "content": "Tóm tắt: Testing ML cần pipelines và kiểm tra data drift."},
]


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        # Insert users
        for u in USERS:
            existing = await session.get(User, u["id"])
            if not existing:
                session.add(User(
                    id=u["id"],
                    email=u["email"],
                    password=u["password"],
                    role=u["role"],
                ))

        await session.commit()

        # Insert papers
        for p in PAPERS:
            existing = await session.get(Paper, p["id"])
            if not existing:
                session.add(
                    Paper(
                        id=p["id"],
                        user_id=p["user_id"],
                        title=p["title"],
                        content=p["content"],
                        file_path=p["file_path"],
                    )
                )

        await session.commit()

        # Insert summaries
        for s in SUMMARIES:
            existing = await session.get(Summary, s["id"])
            if not existing:
                session.add(
                    Summary(id=s["id"], paper_id=s["paper_id"], type=s["type"], content=s["content"])
                )

        await session.commit()


def main() -> None:
    # Only seed when explicitly enabled via ENV variable. Default: false.
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB != true — skipping seeding.")
        return
    asyncio.run(seed())


if __name__ == "__main__":
    main()
