# SUMMARY-PAPER (Hệ thống Tóm tắt Bài báo AI)

Hệ thống tóm tắt văn bản tích hợp AI sử dụng FastAPI, React, và các mô hình NLP (Xử lý ngôn ngữ tự nhiên) chuyên dụng cho việc xử lý các bài báo khoa học, học thuật.

## 📌 Tổng quan dự án
Đây là một ứng dụng web Fullstack được thiết kế dành cho các nhà nghiên cứu, sinh viên và chuyên gia để nhanh chóng tóm tắt các bài báo học thuật. Hệ thống cho phép người dùng tải lên tài liệu PDF, bóc tách văn bản tự động, và sử dụng các mô hình AI/ML để tạo ra các bản tóm tắt ngắn gọn hoặc chi tiết.

Hiện tại, hệ thống đã được xây dựng hoàn chỉnh với Frontend (React Single Page Application), Backend (FastAPI), và cơ sở dữ liệu (Async MySQL). 

## ✨ Tính năng nổi bật
- **Xác thực người dùng:** Hệ thống đăng ký và đăng nhập bảo mật bằng JWT.
- **Quản lý Bài báo:** Tải lên các file tài liệu nghiên cứu (PDF) và tự động trích xuất nội dung văn bản bằng `pypdf`.
- **Tóm tắt bằng AI:** Tích hợp bộ khung (framework) logic ML sẵn sàng để kết nối với các API NLP thật.
- **Lịch sử Tóm tắt:** Lưu trữ và xem lại các bản tóm tắt đã tạo trước đó.
- **Môi trường Container hóa:** Toàn bộ hệ thống được đóng gói bằng Docker Compose, giúp việc phát triển và triển khai trở nên liền mạch.

## 🛠️ Công nghệ sử dụng
- **Frontend:** React, Vite, Axios, React Router.
- **Backend:** Python, FastAPI, SQLAlchemy (Async), PyMySQL, Alembic, PyPDF.
- **Database:** MySQL 8.0.
- **Triển khai (Deployment):** Docker, Docker Compose.

## 📂 Cấu trúc thư mục
```text
SUMMARY-PAPER/
├── backend/                # Mã nguồn ứng dụng FastAPI
│   ├── alembic/            # Quản lý lịch sử thay đổi cơ sở dữ liệu (Migrations)
│   ├── app/                # Logic cốt lõi (API, DB, ML, Models)
│   ├── Dockerfile          # Cấu hình build container Backend
│   └── requirements.txt    # Các thư viện Python cần thiết
├── frontend/               # Mã nguồn React + Vite
│   ├── src/                # Components, Pages, và Services
│   ├── Dockerfile          # Cấu hình build container Frontend
│   └── package.json        # Các thư viện Node.js cần thiết
├── docker-compose.yml      # Tệp cấu hình chạy đồng thời Frontend, Backend và Database
└── claude.md               # Tài liệu chi tiết về kiến trúc hệ thống và quy tắc code
```

## 🚀 Hướng dẫn Cài đặt & Chạy dự án

### Yêu cầu hệ thống
- Cài đặt sẵn [Docker](https://www.docker.com/) và Docker Compose.
- (Tùy chọn) Python 3.10+ và Node.js 18+ nếu muốn chạy không dùng Docker.

### Chạy bằng Docker Compose (Khuyên dùng)
Cách nhanh nhất và dễ nhất để khởi chạy hệ thống là sử dụng Docker.

1. **Clone repository về máy:**
   ```bash
   git clone <repository-url>
   cd SUMMARY-PAPER
   ```

2. **Thiết lập biến môi trường (Environment Variables):**
   Vì lý do bảo mật, file `.env.docker` không được push lên Git. Bạn cần tự tạo nó dựa trên file mẫu:
   ```bash
   # Copy từ file example
   cp backend/.env.example backend/.env.docker
   ```

3. **Khởi chạy ứng dụng:**
   ```bash
   docker-compose up --build -d
   ```
   *Lưu ý: Lệnh này sẽ tự động build frontend React, khởi tạo backend FastAPI, thiết lập database MySQL, và tự động chạy Alembic migrations (`alembic upgrade head`) để tạo các bảng trong CSDL.*

4. **Truy cập ứng dụng:**
   - **Giao diện Frontend (UI):** `http://localhost:5173`
   - **Tài liệu API Backend (Swagger):** `http://localhost:8000/docs`
   - **Cổng kết nối Database:** `3307` (đã map ra máy host)

### Hướng dẫn chạy Local (Không dùng Docker)

Nếu bạn muốn chạy từng service riêng biệt:

**1. Cơ sở dữ liệu (Database)**
Đảm bảo bạn đang chạy MySQL server trên máy. Cập nhật thông tin kết nối trong file `backend/.env.dev` cho phù hợp.

**2. Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**3. Frontend**
```bash
cd frontend
npm install
npm run dev
```

## 🔍 Phân tích Luồng hoạt động (Workflow)
Hệ thống hiện tại hoạt động theo luồng như sau:
1. **Xác thực (Authentication):** Người dùng đăng ký/đăng nhập. Backend kiểm tra và cấp phát mã JWT. Frontend lưu mã này vào `localStorage` và tự động gắn vào các request tiếp theo thông qua Axios interceptors.
2. **Tải lên tài liệu (Upload):** Người dùng tải lên file PDF tại trang `UploadSummary`. File được gửi đến endpoint `/papers/upload` của Backend. Tại đây, text được bóc tách bằng thư viện `pypdf` và lưu vào MySQL.
3. **Tóm tắt (Summarization):** Frontend gọi endpoint `/summaries/generate` cùng với `paper_id`. File `ml/summarizer.py` của Backend sẽ xử lý văn bản. *(Lưu ý: Chức năng tóm tắt hiện tại đang sử dụng Mock API giả lập. Cần thay thế bằng API gọi Model AI thật trong tệp `summarizer.py` khi tích hợp).*
4. **Lịch sử (History):** Các bản tóm tắt được lưu vào CSDL và người dùng có thể xem lại tại trang `History`.

## ⚠️ Các vấn đề cần lưu ý & Cảnh báo Bảo mật
- **Cấu hình CORS:** Backend hiện đang cho phép tất cả các nguồn truy cập (`allow_origins=["*"]`). Trước khi đưa lên môi trường Production, cần cập nhật file `backend/app/main.py` để chỉ cho phép domain thật của frontend.
- **Tóm tắt bằng AI (ML Summarization):** Logic AI hiện tại đang được làm giả (mock). Cần có URL inference từ đội ngũ làm AI để thay thế hàm giả lập trong `backend/app/ml/summarizer.py`.
- **Lưu trữ JWT:** Token hiện đang được lưu tại `localStorage`. Để nâng cao tính bảo mật (chống tấn công XSS), nên cân nhắc chuyển sang lưu token dưới dạng `httpOnly` cookies trong tương lai.

## 🔮 Định hướng Phát triển
- Tích hợp các mô hình AI/NLP thật cho tính năng Tóm tắt Trích xuất (Extractive) và Tóm tắt Tóm lược (Abstractive).
- Thêm Dashboard Power BI để theo dõi số liệu sử dụng ứng dụng, hoạt động người dùng và các chủ đề phổ biến.
- Triển khai Phân quyền (Role-Based Access Control - RBAC) để phân tách vai trò giữa Admin và Người dùng thường.
