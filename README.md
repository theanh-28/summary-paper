# SUMMARY-PAPER (Hệ thống Tóm tắt Bài báo AI)

Hệ thống ứng dụng AI để tự động tóm tắt các tài liệu học thuật và bài báo khoa học. Dự án được xây dựng với kiến trúc Fullstack hiện đại, hỗ trợ xử lý đa định dạng tài liệu, xử lý nền tốc độ cao và phân quyền người dùng chặt chẽ.

## 📌 Tổng quan dự án

SUMMARY-PAPER giúp người dùng tải lên các tài liệu nghiên cứu và nhanh chóng nhận lại bản tóm tắt tiếng Việt ngắn gọn. Hệ thống được thiết kế để chịu tải tốt với cơ chế xử lý nền bằng Redis/ARQ, lưu trữ file an toàn trên Supabase, tích hợp Dashboard phân tích dữ liệu qua Metabase và sẵn sàng chạy trên môi trường Production (Render/Vercel).

## ✨ Tính năng cốt lõi

- **Hỗ trợ Đa định dạng:** Xử lý và trích xuất văn bản từ các file **PDF, DOCX, TXT**.
- **Tóm tắt AI Tự động:** Tích hợp API mô hình AI ngoài để phân tích và tóm tắt tự động nội dung học thuật.
- **Xử lý Nền (Background Processing):** Tích hợp hàng đợi (queue) với **Redis & ARQ** giúp các tác vụ tóm tắt nặng không làm tắc nghẽn server.
- **Phân quyền nâng cao (RBAC):** Hệ thống có 3 cấp độ tài khoản (User, Admin, Root) với các phân quyền truy cập và quản lý dữ liệu khác nhau. Quản trị viên có thể quản lý, khóa hoặc xóa tài khoản.
- **Lưu trữ Cloud:** Upload và lưu trữ tài liệu an toàn trên **Supabase Object Storage**.
- **Analytics Dashboard:** Tích hợp **Metabase Signed Embedding** ngay trong giao diện quản trị viên để theo dõi số liệu thống kê chi tiết.

## 🛠️ Công nghệ sử dụng

- **Frontend:** React, Vite, Axios, React Router, Vanilla CSS.
- **Backend:** Python, FastAPI, SQLAlchemy (Async), PyMySQL, Alembic, Pydantic, ARQ.
- **Cơ sở dữ liệu:** MySQL / TiDB.
- **Queue / Caching:** Redis.
- **Object Storage:** Supabase.
- **Analytics:** Metabase.
- **Triển khai (Deployment):** Docker & Docker Compose (Local), Render (Backend, Worker), Vercel (Frontend).

## 📂 Cấu trúc thư mục

```text
SUMMARY-PAPER/
├── backend/                # API Backend & Background Workers (FastAPI, ARQ)
│   ├── alembic/            # Quản lý lịch sử thay đổi Database (Migrations)
│   ├── app/                # Logic hệ thống (API, Models, Repositories, ML)
│   ├── requirements.txt    # Thư viện Python
│   └── worker.py           # Background Worker xử lý hàng đợi Redis
├── frontend/               # Ứng dụng giao diện người dùng (React + Vite)
│   ├── src/                # Components, Pages, Context, Services
│   └── package.json        # Thư viện Node.js
├── database/               # Scripts khởi tạo DB (nếu có)
└── docker-compose.yml      # Cấu hình khởi chạy toàn bộ dịch vụ cho môi trường Local
```

## 🚀 Hướng dẫn Cài đặt & Khởi chạy (Local)

Cách dễ nhất để phát triển và kiểm thử ở môi trường Local là sử dụng **Docker Compose**.

### Yêu cầu hệ thống
- Đã cài đặt [Docker](https://www.docker.com/) và Docker Compose.

### 1. Cấu hình biến môi trường
Bạn cần tạo các file `.env` cho backend và frontend dựa trên file mẫu `.env.example`. 

**Backend (`backend/.env.docker`):**
Cung cấp các thông tin thiết yếu như chuỗi kết nối MySQL, URL kết nối Redis, thông tin Supabase, cấu hình Metabase và API key của AI Model.

### 2. Khởi chạy bằng Docker
Tại thư mục gốc của dự án, mở Terminal và chạy lệnh:
```bash
docker-compose up --build
```

Lệnh này sẽ tự động:
- Khởi tạo Container cho Database (MySQL).
- Khởi tạo Redis cho hàng đợi tác vụ.
- Build và chạy Backend API (FastAPI) trên cổng `8000`.
- Chạy Background Worker (ARQ) để chờ xử lý tóm tắt.
- Build và chạy Frontend (React/Vite) trên cổng `5173`.
- Tự động chạy Alembic migrations để tạo cấu trúc bảng dữ liệu.

### 3. Truy cập hệ thống
- **Giao diện Web:** `http://localhost:5173`
- **Tài liệu API (Swagger UI):** `http://localhost:8000/docs`

## 🔍 Kiến trúc & Luồng hoạt động (Workflow)

1. **Xác thực:** Đăng nhập qua API, Backend trả về JWT token. Frontend lưu JWT ở bộ nhớ cục bộ để xác thực các request.
2. **Tải tài liệu:** Người dùng upload file (PDF, DOCX, TXT). Backend lưu file lên Supabase Storage, lưu thông tin metadata vào Database với trạng thái `uploaded`.
3. **Đẩy vào Hàng đợi (Queue):** Backend gửi một Job tóm tắt vào hàng đợi Redis thông qua ARQ.
4. **Xử lý ngầm (Worker):** ARQ Worker nhận Job, tải nội dung từ Supabase, bóc tách text (bằng `pypdf`, `python-docx`), và gửi text sang API của AI Model để lấy kết quả. 
5. **Hoàn tất:** Khi AI xử lý xong, Worker cập nhật trạng thái bài báo thành `completed` và lưu bản tóm tắt vào Database.
6. **Thống kê:** Admin có thể xem toàn bộ biểu đồ, số liệu người dùng thông qua Dashboard Metabase được nhúng an toàn qua cơ chế Signed JWT.

## 📦 Triển khai (Production)

Hệ thống đã được tinh chỉnh để sẵn sàng triển khai thực tế:
- **TiDB Serverless** thay thế MySQL cục bộ.
- **Render** dùng để host API Backend (Web Service) và Background Worker (Background Service). Cần kết nối với Redis trên đám mây (ví dụ: Upstash Redis).
- **Vercel** dùng để host Frontend tĩnh cực nhanh.
- Biến môi trường trên Production được quản lý trực tiếp qua giao diện của Render và Vercel.
