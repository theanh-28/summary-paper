-- =============================================================================
-- Init script cho MySQL container
-- Chạy tự động lần đầu tiên khi container được tạo ra.
-- File này được mount vào /docker-entrypoint-initdb.d/ trong docker-compose.
--
-- Tạo 2 databases:
--   1. summary_paper   — Application database (backend FastAPI sử dụng)
--   2. metabase_appdb   — Metabase internal metadata database
-- =============================================================================

-- Database summary_paper đã được tạo bởi MYSQL_DATABASE env var trong docker-compose.
-- Chỉ cần tạo thêm metabase_appdb.

CREATE DATABASE IF NOT EXISTS metabase_appdb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Cấp quyền cho summary_user trên cả 2 databases
GRANT ALL PRIVILEGES ON summary_paper.* TO 'summary_user'@'%';
GRANT ALL PRIVILEGES ON metabase_appdb.* TO 'summary_user'@'%';
FLUSH PRIVILEGES;
