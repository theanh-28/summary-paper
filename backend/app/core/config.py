"""Application configuration loaded from environment variables."""
from __future__ import annotations

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Database ---
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # --- JWT ---
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # --- CORS ---
    # Comma-separated list of allowed origins, e.g. "http://localhost:5173,https://app.example.com"
    cors_origins: str = "http://localhost:5173"

    # --- Metabase Embedding ---
    # METABASE_SITE_URL phải là URL mà BROWSER truy cập được (không phải Docker internal)
    # vì embed URL sẽ được load trong iframe bởi trình duyệt của user.
    metabase_site_url: str = "http://localhost:3000"
    metabase_secret_key: str = ""  # Set via env var METABASE_SECRET_KEY
    metabase_admin_dashboard_id: int = 1  # ID of admin dashboard in Metabase
    metabase_user_dashboard_id: int = 2   # ID of user dashboard in Metabase

    # --- AI API ---
    # Đọc URL từ file .env, nếu không có sẽ lấy giá trị mặc định này
    ai_api_url: str = "https://taismiel-summper.hf.space"
    hf_token: str = ""

    # --- Redis (Background Worker) ---
    redis_url: str = "redis://localhost:6379"

    # --- Supabase Object Storage ---
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_bucket: str = "papers"

    # --- General ---
    debug: bool = False  # Default OFF for production safety; enable via DEBUG=true

    @property
    def database_url(self) -> str:
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    class Config:
        env_file = os.getenv("ENV_FILE", ".env.dev")


settings = Settings()
