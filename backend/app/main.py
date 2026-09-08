from fastapi import FastAPI

from app.api.events import router as events_router
from app.api.road_issues import router as road_issues_router
from app.api.traffic import router as traffic_router
from app.api.incidents import router as incidents_router
from app.api.websocket import router as websocket_router


app = FastAPI(
    title="Smart Bus Intelligence API",
    description="Backend for the Smart Bus Urban Sensing Platform",
    version="1.0.0"
)

app.include_router(events_router)
app.include_router(road_issues_router)
app.include_router(traffic_router)
app.include_router(incidents_router)
app.include_router(websocket_router)


@app.get("/")
async def root():
    return {
        "message": "Smart Bus Intelligence API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }