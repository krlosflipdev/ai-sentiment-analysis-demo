"""Statistics service for aggregated sentiment data."""

from datetime import datetime
from typing import Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.sentiment import SentimentStats, TimelinePoint


class StatsService:
    """Service for sentiment statistics and aggregations.

    Args:
        db: The MongoDB database instance.
    """

    COLLECTION_NAME = "sentiments"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[self.COLLECTION_NAME]

    async def get_summary(self) -> SentimentStats:
        """Get overall sentiment statistics.

        Returns:
            Aggregated sentiment statistics.
        """
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": 1},
                    "positive": {
                        "$sum": {"$cond": [{"$eq": ["$sentiment", "positive"]}, 1, 0]}
                    },
                    "negative": {
                        "$sum": {"$cond": [{"$eq": ["$sentiment", "negative"]}, 1, 0]}
                    },
                    "neutral": {
                        "$sum": {"$cond": [{"$eq": ["$sentiment", "neutral"]}, 1, 0]}
                    },
                    "avg_score": {"$avg": "$score"},
                }
            }
        ]

        results = await self.collection.aggregate(pipeline).to_list(1)

        if not results:
            # Return empty stats if no data
            return SentimentStats(
                total_count=0,
                positive_count=0,
                negative_count=0,
                neutral_count=0,
                positive_percentage=0.0,
                negative_percentage=0.0,
                neutral_percentage=0.0,
                average_score=0.0,
            )

        result = results[0]
        total = result["total"]

        return SentimentStats(
            total_count=total,
            positive_count=result["positive"],
            negative_count=result["negative"],
            neutral_count=result["neutral"],
            positive_percentage=round((result["positive"] / total) * 100, 2)
            if total > 0
            else 0.0,
            negative_percentage=round((result["negative"] / total) * 100, 2)
            if total > 0
            else 0.0,
            neutral_percentage=round((result["neutral"] / total) * 100, 2)
            if total > 0
            else 0.0,
            average_score=round(result["avg_score"] or 0.0, 4),
        )

    async def get_timeline(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        granularity: str = "day",
    ) -> List[TimelinePoint]:
        """Get sentiment counts over time for charting.

        Args:
            date_from: Start date filter (inclusive).
            date_to: End date filter (inclusive).
            granularity: Time bucket size ("hour", "day", "week", "month").

        Returns:
            List of timeline data points sorted by date.
        """
        # Build match stage for date filtering
        match_stage: Dict = {}
        if date_from or date_to:
            match_stage["created_at"] = {}
            if date_from:
                match_stage["created_at"]["$gte"] = date_from
            if date_to:
                match_stage["created_at"]["$lte"] = date_to

        # Determine date format based on granularity
        date_formats = {
            "hour": "%Y-%m-%dT%H:00:00",
            "day": "%Y-%m-%d",
            "week": "%Y-W%V",
            "month": "%Y-%m",
        }
        date_format = date_formats.get(granularity, "%Y-%m-%d")

        pipeline = [
            {"$match": match_stage} if match_stage else {"$match": {}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {"format": date_format, "date": "$created_at"}
                    },
                    "positive": {
                        "$sum": {"$cond": [{"$eq": ["$sentiment", "positive"]}, 1, 0]}
                    },
                    "negative": {
                        "$sum": {"$cond": [{"$eq": ["$sentiment", "negative"]}, 1, 0]}
                    },
                    "neutral": {
                        "$sum": {"$cond": [{"$eq": ["$sentiment", "neutral"]}, 1, 0]}
                    },
                    "total": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        results = await self.collection.aggregate(pipeline).to_list(None)

        return [
            TimelinePoint(
                date=doc["_id"],
                positive=doc["positive"],
                negative=doc["negative"],
                neutral=doc["neutral"],
                total=doc["total"],
            )
            for doc in results
        ]
