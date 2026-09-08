from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.event import Event
from app.models.road_issue import RoadIssue
from app.models.traffic_hotspot import TrafficHotspot
from app.models.incident import Incident


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db)
):
    total_events = await db.scalar(
        select(func.count(Event.id))
    )

    active_road_issues = await db.scalar(
        select(func.count(RoadIssue.id))
    )

    traffic_hotspots = await db.scalar(
        select(func.count(TrafficHotspot.id))
    )

    active_incidents = await db.scalar(
        select(func.count(Incident.id)).where(
            Incident.status != "RESOLVED"
        )
    )

    high_severity_issues = await db.scalar(
        select(func.count(RoadIssue.id)).where(
            RoadIssue.severity == "HIGH"
        )
    )

    high_congestion_hotspots = await db.scalar(
        select(func.count(TrafficHotspot.id)).where(
            TrafficHotspot.congestion_level == "HIGH"
        )
    )

    return {
        "total_events": total_events or 0,
        "active_road_issues": active_road_issues or 0,
        "traffic_hotspots": traffic_hotspots or 0,
        "active_incidents": active_incidents or 0,
        "high_severity_issues": high_severity_issues or 0,
        "high_congestion_hotspots": high_congestion_hotspots or 0
    }