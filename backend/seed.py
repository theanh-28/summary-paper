"""Dynamic Seed script to insert large-scale sample data for local testing.

Run with: python seed.py
"""
import asyncio
import os
import random
from datetime import datetime, timedelta

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.paper import Paper
from app.models.summary import Summary

# Mật khẩu mặc định: "123456"
DEFAULT_PASSWORD = "Ap59QUkIqYuM9nS1Wm/C+w==$xw+nWY59tEfZUp1I3cGUy3UkwHVT8M1PGI97jJhTaeo="

TOPICS = [
    "Học máy cơ bản", "Mạng nơ-ron sâu", "Xử lý ngôn ngữ tự nhiên", "Thị giác máy tính",
    "Blockchain và Smart Contract", "Điện toán đám mây", "Bảo mật Zero-Trust", "DevOps & CI/CD",
    "Phân tích dữ liệu lớn", "Trí tuệ nhân tạo tạo sinh (GenAI)", "Công nghệ mRNA", 
    "Chỉnh sửa gen CRISPR", "Hệ vi sinh vật đường ruột", "Ung thư học phân tử",
    "Kinh tế vĩ mô", "Tài chính phi tập trung (DeFi)", "Đầu tư giá trị", "Kinh tế tuần hoàn",
    "Lịch sử Đế chế La Mã", "Cách mạng Công nghiệp", "Chiến tranh Lạnh",
    "Năng lượng tái tạo", "Khí hậu và Nước biển dâng", "Xe điện và Trạm sạc",
    "Giáo dục thời đại số", "Tâm lý học hành vi", "Triết học Khắc kỷ"
]

ERROR_MESSAGES = [
    "Lỗi trích xuất: PDF là dạng ảnh scan không chứa văn bản.",
    "Lỗi AI: Timeout khi gọi API mô hình ngôn ngữ.",
    "Lỗi định dạng: File bị hỏng hoặc mã hóa mật khẩu.",
    "Lỗi dung lượng: Vượt quá giới hạn token của AI."
]

def random_date(days_back=30):
    """Tạo ngày ngẫu nhiên trong vòng X ngày qua để test biểu đồ Metabase."""
    return datetime.utcnow() - timedelta(days=random.randint(0, days_back), hours=random.randint(0, 23), minutes=random.randint(0, 59))

async def seed() -> None:
    async with AsyncSessionLocal() as session:
        print("Đang tạo Users...")
        # 1. TẠO USERS (1 Root, 2 Admin, 35 Users = 38 Users)
        users_data = [
            {"id": 1, "email": "admin@example.com", "full_name": "Quản trị viên Cấp cao", "role": "root"},
            {"id": 2, "email": "manager1@example.com", "full_name": "Quản lý Dự án", "role": "admin"},
            {"id": 3, "email": "manager2@example.com", "full_name": "Quản lý Nội dung", "role": "admin"},
        ]
        
        # Sinh thêm 35 user thường
        for i in range(4, 39):
            users_data.append({
                "id": i,
                "email": f"user{i}@example.com",
                "full_name": f"Người dùng Nghiên cứu số {i}",
                "role": "user"
            })

        for u_data in users_data:
            existing = await session.get(User, u_data["id"])
            if not existing:
                u_data["password"] = DEFAULT_PASSWORD
                u_data["is_active"] = True
                u_data["created_at"] = random_date(60) # User đăng ký rải rác 60 ngày qua
                u_data["last_login"] = random_date(5)
                session.add(User(**u_data))
        await session.commit()

        print("Đang tạo Papers (> 250 records)...")
        # 2. TẠO PAPERS (Khoảng 250 bài báo)
        papers_data = []
        status_weights = ["completed"] * 70 + ["failed"] * 15 + ["processing"] * 10 + ["uploaded"] * 5
        
        paper_id_counter = 1
        # Phân bổ đều bài báo cho 35 user (ID từ 4 đến 38)
        for user_id in range(4, 39):
            # Mỗi user có từ 3 đến 12 bài báo
            num_papers_for_user = random.randint(3, 12)
            for _ in range(num_papers_for_user):
                status = random.choice(status_weights)
                c_date = random_date(30)
                
                paper = {
                    "id": paper_id_counter,
                    "user_id": user_id,
                    "title": f"Báo cáo nghiên cứu: {random.choice(TOPICS)} - Phần {random.randint(1, 5)}",
                    "content": "Nội dung văn bản thô trích xuất từ PDF giả định...",
                    "file_path": f"/uploads/mock_file_{paper_id_counter}.pdf",
                    "page_count": random.randint(3, 80),
                    "status": status,
                    "created_at": c_date,
                    "updated_at": c_date
                }

                # Giả lập logic cho từng trạng thái
                if status == "completed":
                    processing_time = random.randint(10, 180)
                    paper["processing_time_seconds"] = processing_time
                    paper["updated_at"] = c_date + timedelta(seconds=processing_time)
                elif status == "failed":
                    processing_time = random.randint(2, 30)
                    paper["processing_time_seconds"] = processing_time
                    paper["updated_at"] = c_date + timedelta(seconds=processing_time)
                    paper["error_message"] = random.choice(ERROR_MESSAGES)

                papers_data.append(paper)
                paper_id_counter += 1

        for p_data in papers_data:
            existing = await session.get(Paper, p_data["id"])
            if not existing:
                session.add(Paper(**p_data))
        await session.commit()

        print("Đang tạo Summaries...")
        # 3. TẠO SUMMARIES (Chỉ áp dụng cho các paper có status = 'completed')
        summary_id_counter = 1
        summaries_data = []
        for p in papers_data:
            if p["status"] == "completed":
                # Một số bài báo có 1 summary, một số có 2 (dạng ngắn và dạng dài)
                num_summaries = random.choice([1, 2])
                for _ in range(num_summaries):
                    s_type = random.choice(["short", "detailed"])
                    summaries_data.append({
                        "id": summary_id_counter,
                        "paper_id": p["id"],
                        "type": s_type,
                        "content": f"Đây là nội dung tóm tắt ({s_type}) được AI tạo ra cho bài báo số {p['id']}. Kết quả phân tích cho thấy các luận điểm chính rất rõ ràng..."
                    })
                    summary_id_counter += 1

        for s_data in summaries_data:
            existing = await session.get(Summary, s_data["id"])
            if not existing:
                session.add(Summary(**s_data))
        await session.commit()

        print(f"✅ Seeding hoàn tất! Đã tạo: 38 Users, {len(papers_data)} Papers, {len(summaries_data)} Summaries.")


def main() -> None:
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB != true — skipping seeding.")
        return
    asyncio.run(seed())

if __name__ == "__main__":
    main()