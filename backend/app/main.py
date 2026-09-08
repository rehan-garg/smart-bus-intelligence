from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

from app.api.events import router as events_router
from app.api.road_issues import router as road_issues_router
from app.api.traffic import router as traffic_router
from app.api.incidents import router as incidents_router
from app.api.websocket import router as websocket_router
from app.api.dashboard import router as dashboard_router


app = FastAPI(
    title="Smart Bus Intelligence API",
    description="Backend for the Smart Bus Urban Sensing Platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(events_router)
app.include_router(road_issues_router)
app.include_router(traffic_router)
app.include_router(incidents_router)
app.include_router(websocket_router)
app.include_router(dashboard_router)


@app.get("/")
async def root():
    return {
        "message": "Smart Bus Intelligence API is running"
    }


@app.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db)
):
    try:
        await db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }