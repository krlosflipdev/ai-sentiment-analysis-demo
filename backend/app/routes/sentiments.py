"""Sentiment API endpoints."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import settings
from app.database import get_database
from app.models.base import PaginatedResponse, PaginationMeta, SingleResponse
from app.models.sentiment import SentimentFilter, SentimentLabel, SentimentRecord
from app.services.sentiment_service import SentimentService

router = APIRouter(prefix="/api/v1/sentiments", tags=["Sentiments"])


@router.get("", response_model=PaginatedResponse[SentimentRecord])
async def list_sentiments(
    page: int = Query(1, ge=1, description="Page number"),
    limit: Optional[int] = Query(
        default=None,
        ge=1,
        le=100,
        description="Items per page",
    ),
    sentiment: Optional[SentimentLabel] = Query(None, description="Filter by sentiment"),
    source: Optional[str] = Query(None, description="Filter by source"),
    date_from: Optional[datetime] = Query(None, description="Filter from date (ISO 8601)"),
    date_to: Optional[datetime] = Query(None, description="Filter to date (ISO 8601)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> PaginatedResponse[SentimentRecord]:
    """Get paginated list of sentiment records.

    Args:
        page: Page number (1-indexed).
        limit: Number of items per page (max 100).
        sentiment: Optional filter by sentiment label.
        source: Optional filter by data source.
        date_from: Optional filter for records after this date.
        date_to: Optional filter for records before this date.
        db: Database instance (injected).

    Returns:
        Paginated list of sentiment records with metadata.
    """
    if limit is None:
        limit = settings.default_page_size

    service = SentimentService(db)
    filters = SentimentFilter(
        sentiment=sentiment,
        source=source,
        date_from=date_from,
        date_to=date_to,
    )

    records, total = await service.get_paginated(page, limit, filters)
    total_pages = (total + limit - 1) // limit if total > 0 else 0

    return PaginatedResponse(
        data=records,
        meta=PaginationMeta(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


@router.get("/{sentiment_id}", response_model=SingleResponse[SentimentRecord])
async def get_sentiment(
    sentiment_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> SingleResponse[SentimentRecord]:
    """Get a single sentiment record by ID.

    Args:
        sentiment_id: The sentiment record ID.
        db: Database instance (injected).

    Returns:
        The sentiment record wrapped in a response object.

    Raises:
        404: If the sentiment record is not found.
        422: If the ID format is invalid.
    """
    service = SentimentService(db)
    record = await service.get_by_id(sentiment_id)

    return SingleResponse(data=record)
