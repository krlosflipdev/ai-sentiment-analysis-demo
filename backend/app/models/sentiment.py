"""Sentiment domain models."""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

SentimentLabel = Literal["positive", "negative", "neutral"]


class SentimentRecord(BaseModel):
    """A single sentiment analysis result.

    Attributes:
        id: Unique identifier (MongoDB ObjectId as string).
        text: The analyzed text content.
        sentiment: Sentiment classification label.
        score: Confidence score between 0 and 1.
        source: Data source (e.g., twitter, reddit, manual).
        created_at: Timestamp when the analysis was performed.
    """

    id: str = Field(..., description="Unique identifier")
    text: str = Field(..., description="Analyzed text content")
    sentiment: SentimentLabel = Field(..., description="Sentiment classification")
    score: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")
    source: str = Field(..., description="Data source")
    created_at: datetime = Field(..., description="Timestamp of analysis")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "text": "I love this product!",
                "sentiment": "positive",
                "score": 0.95,
                "source": "twitter",
                "created_at": "2026-01-29T10:30:00Z",
            }
        }
    }


class SentimentStats(BaseModel):
    """Aggregated sentiment statistics.

    Attributes:
        total_count: Total number of sentiment records.
        positive_count: Number of positive sentiments.
        negative_count: Number of negative sentiments.
        neutral_count: Number of neutral sentiments.
        positive_percentage: Percentage of positive sentiments.
        negative_percentage: Percentage of negative sentiments.
        neutral_percentage: Percentage of neutral sentiments.
        average_score: Average confidence score across all records.
    """

    total_count: int = Field(..., ge=0, description="Total records")
    positive_count: int = Field(..., ge=0, description="Positive sentiment count")
    negative_count: int = Field(..., ge=0, description="Negative sentiment count")
    neutral_count: int = Field(..., ge=0, description="Neutral sentiment count")
    positive_percentage: float = Field(
        ..., ge=0, le=100, description="Positive percentage"
    )
    negative_percentage: float = Field(
        ..., ge=0, le=100, description="Negative percentage"
    )
    neutral_percentage: float = Field(
        ..., ge=0, le=100, description="Neutral percentage"
    )
    average_score: float = Field(..., ge=0, le=1, description="Average confidence score")


class TimelinePoint(BaseModel):
    """A single point in the sentiment timeline.

    Attributes:
        date: Date string in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:00:00).
        positive: Count of positive sentiments.
        negative: Count of negative sentiments.
        neutral: Count of neutral sentiments.
        total: Total count for this time period.
    """

    date: str = Field(..., description="Date/time bucket")
    positive: int = Field(..., ge=0, description="Positive count")
    negative: int = Field(..., ge=0, description="Negative count")
    neutral: int = Field(..., ge=0, description="Neutral count")
    total: int = Field(..., ge=0, description="Total count")


class SentimentFilter(BaseModel):
    """Filter parameters for querying sentiments.

    Attributes:
        sentiment: Filter by sentiment label.
        source: Filter by data source.
        date_from: Filter records created on or after this date.
        date_to: Filter records created on or before this date.
    """

    sentiment: Optional[SentimentLabel] = None
    source: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


class SentimentCreate(BaseModel):
    """Request model for creating a sentiment record.

    Attributes:
        text: The text that was analyzed.
        sentiment: The sentiment classification result.
        score: Confidence score from the model (0-1).
        source: Data source identifier (e.g., twitter, reddit).
        source_id: Optional unique ID from the source for deduplication.
    """

    text: str = Field(..., min_length=1, max_length=5000, description="Analyzed text")
    sentiment: SentimentLabel = Field(..., description="Sentiment classification")
    score: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")
    source: str = Field(..., min_length=1, max_length=50, description="Data source")
    source_id: Optional[str] = Field(
        None, max_length=100, description="Unique ID from source for deduplication"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "I love this product!",
                "sentiment": "positive",
                "score": 0.95,
                "source": "twitter",
                "source_id": "1234567890",
            }
        }
    }


class SentimentBatchCreate(BaseModel):
    """Request model for batch creating sentiment records.

    Attributes:
        records: List of sentiment records to create (max 100).
    """

    records: List[SentimentCreate] = Field(
        ..., min_length=1, max_length=100, description="Records to create"
    )


class BatchCreateResult(BaseModel):
    """Response model for batch create operation.

    Attributes:
        created_count: Number of records successfully created.
        skipped_count: Number of records skipped (duplicates).
    """

    created_count: int = Field(..., ge=0, description="Records created")
    skipped_count: int = Field(..., ge=0, description="Duplicates skipped")
