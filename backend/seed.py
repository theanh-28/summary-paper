"""Seed script to insert sample data from init.sql for local testing.

Run with: python -m backend.seed  (from repository root) or
python backend/seed.py

This script is idempotent: it checks primary keys before inserting.
"""
import asyncio
from typing import List, Dict

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.paper import Paper
from app.models.summary import Summary


USERS: List[Dict] = [
    {"id": 2, "email": "user1@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo="},
    {"id": 3, "email": "user2@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo="},
    {"id": 4, "email": "user3@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo="},
    {"id": 5, "email": "user4@example.com", "password": "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo="},
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
]


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        # Insert users
        for u in USERS:
            existing = await session.get(User, u["id"])
            if not existing:
                session.add(User(id=u["id"], email=u["email"], password=u["password"]))

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
    asyncio.run(seed())


if __name__ == "__main__":
    main()
