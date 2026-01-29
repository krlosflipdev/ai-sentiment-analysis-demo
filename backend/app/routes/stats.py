"""Statistics API endpoints."""

from datetime import datetime
from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.models.base import SingleResponse
from app.models.sentiment import SentimentStats, TimelinePoint
from app.services.stats_service import StatsService

router = APIRouter(prefix="/api/v1/stats", tags=["Statistics"])


@router.get("/summary", response_model=SingleResponse[SentimentStats])
async def get_stats_summary(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> SingleResponse[SentimentStats]:
    """Get aggregated sentiment statistics.

    Returns overall counts and percentages for each sentiment type,
    along with the average confidence score.

    Args:
        db: Database instance (injected).

    Returns:
        Aggregated sentiment statistics.
    """
    service = StatsService(db)
    stats = await service.get_summary()

    return SingleResponse(data=stats)


@router.get("/timeline", response_model=SingleResponse[List[TimelinePoint]])
async def get_stats_timeline(
    date_from: Optional[datetime] = Query(None, description="Start date (ISO 8601)"),
    date_to: Optional[datetime] = Query(None, description="End date (ISO 8601)"),
    granularity: Literal["hour", "day", "week", "month"] = Query(
        "day", description="Time bucket granularity"
    ),
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> SingleResponse[List[TimelinePoint]]:
    """Get sentiment counts over time for charting.

    Returns time series data with counts for each sentiment type,
    grouped by the specified granularity.

    Args:
        date_from: Optional start date filter.
        date_to: Optional end date filter.
        granularity: Time bucket size (hour, day, week, month).
        db: Database instance (injected).

    Returns:
        List of timeline data points sorted by date.
    """
    service = StatsService(db)
    timeline = await service.get_timeline(date_from, date_to, granularity)

    return SingleResponse(data=timeline)
