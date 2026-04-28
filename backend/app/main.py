from fastapi import FastAPI

from app.api.paper_routes import router as paper_router
from app.api.routes import router as health_router
from app.api.summary_routes import router as summary_router
from app.api.user_routes import router as user_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Backend structure placeholder"}


app.include_router(health_router)
app.include_router(user_router)
app.include_router(paper_router)
app.include_router(summary_router)
