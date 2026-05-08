"""FastAPI application entry point with CORS, logging, and exception handling."""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.admin_routes import router as admin_router
from app.api.auth_routes import router as auth_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.paper_routes import router as paper_router
from app.api.routes import router as health_router
from app.api.summary_routes import router as summary_router
from app.api.user_routes import router as user_router
from app.core.config import settings

# ---------------------------------------------------------------------------
# Logging — structured logging cho toàn bộ application
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Summary Paper API",
    version="1.0.0",
    description="AI-powered paper summarization platform with RBAC and Metabase analytics.",
    docs_url="/docs" if settings.debug else None,      # Ẩn Swagger trong production
    redoc_url="/redoc" if settings.debug else None,     # Ẩn ReDoc trong production
)

# ---------------------------------------------------------------------------
# CORS — cho phép Frontend (React) gọi API từ origin khác
# Cấu hình qua env var CORS_ORIGINS (comma-separated list).
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# ---------------------------------------------------------------------------
# Global exception handler — bắt tất cả unhandled exceptions
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Bắt tất cả exception chưa xử lý, log chi tiết nhưng trả về
    message an toàn cho client (không lộ stack trace).
    """
    logger.error(
        "Unhandled exception on %s %s: %s",
        request.method,
        request.url.path,
        str(exc),
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/")
async def root():
    return {"message": "Summary Paper API is running"}


# ---------------------------------------------------------------------------
# Register routers
# ---------------------------------------------------------------------------
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(paper_router)
app.include_router(summary_router)
app.include_router(admin_router)
app.include_router(dashboard_router)

logger.info("Summary Paper API started (debug=%s)", settings.debug)
