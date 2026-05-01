from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth_routes import router as auth_router
from app.api.paper_routes import router as paper_router
from app.api.routes import router as health_router
from app.api.summary_routes import router as summary_router
from app.api.user_routes import router as user_router

app = FastAPI(title="Summary Paper API", version="0.1.0")

# ---------------------------------------------------------------------------
# CORS — cho phép Frontend (React) gọi API từ origin khác
# Khi deploy production, thay ["*"] bằng domain thật, ví dụ:
#   ["https://summary-paper.yourdomain.com"]
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: Đổi thành domain cụ thể khi production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Summary Paper API is running"}


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(paper_router)
app.include_router(summary_router)
