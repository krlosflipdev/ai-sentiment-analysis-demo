"""Sentiment service for database operations."""

from typing import Dict, List, Tuple

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.exceptions import NotFoundError, ValidationError
from app.models.sentiment import SentimentFilter, SentimentRecord


class SentimentService:
    """Service for sentiment record operations.

    Args:
        db: The MongoDB database instance.
    """

    COLLECTION_NAME = "sentiments"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[self.COLLECTION_NAME]

    async def get_paginated(
        self,
        page: int,
        limit: int,
        filters: SentimentFilter,
    ) -> Tuple[List[SentimentRecord], int]:
        """Get paginated sentiment records with optional filters.

        Args:
            page: Page number (1-indexed).
            limit: Number of items per page.
            filters: Optional filter parameters.

        Returns:
            Tuple of (list of sentiment records, total count).
        """
        query = self._build_filter_query(filters)

        # Get total count for pagination
        total = await self.collection.count_documents(query)

        # Get paginated results, sorted by created_at descending
        skip = (page - 1) * limit
        cursor = (
            self.collection.find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )

        records = []
        async for doc in cursor:
            records.append(self._doc_to_model(doc))

        return records, total

    async def get_by_id(self, sentiment_id: str) -> SentimentRecord:
        """Get a single sentiment record by ID.

        Args:
            sentiment_id: The sentiment record ID (MongoDB ObjectId as string).

        Returns:
            The sentiment record.

        Raises:
            ValidationError: If the ID format is invalid.
            NotFoundError: If no record is found with the given ID.
        """
        try:
            object_id = ObjectId(sentiment_id)
        except InvalidId:
            raise ValidationError(f"Invalid sentiment ID format: {sentiment_id}")

        doc = await self.collection.find_one({"_id": object_id})

        if not doc:
            raise NotFoundError("Sentiment", sentiment_id)

        return self._doc_to_model(doc)

    def _build_filter_query(self, filters: SentimentFilter) -> Dict:
        """Build MongoDB query from filter parameters.

        Args:
            filters: The filter parameters.

        Returns:
            MongoDB query dictionary.
        """
        query: Dict = {}

        if filters.sentiment:
            query["sentiment"] = filters.sentiment

        if filters.source:
            query["source"] = filters.source

        if filters.date_from or filters.date_to:
            query["created_at"] = {}
            if filters.date_from:
                query["created_at"]["$gte"] = filters.date_from
            if filters.date_to:
                query["created_at"]["$lte"] = filters.date_to

        return query

    def _doc_to_model(self, doc: Dict) -> SentimentRecord:
        """Convert MongoDB document to Pydantic model.

        Args:
            doc: MongoDB document dictionary.

        Returns:
            SentimentRecord Pydantic model.
        """
        return SentimentRecord(
            id=str(doc["_id"]),
            text=doc["text"],
            sentiment=doc["sentiment"],
            score=doc["score"],
            source=doc["source"],
            created_at=doc["created_at"],
        )
