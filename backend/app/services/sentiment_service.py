"""Sentiment service for database operations."""

from datetime import datetime, timezone
from typing import Dict, List, Tuple

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.exceptions import NotFoundError, ValidationError
from app.models.sentiment import (
    BatchCreateResult,
    SentimentCreate,
    SentimentFilter,
    SentimentRecord,
)


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

    async def create(self, data: SentimentCreate) -> SentimentRecord:
        """Create a new sentiment record.

        Args:
            data: The sentiment data to create.

        Returns:
            The created sentiment record.
        """
        doc = {
            "text": data.text,
            "sentiment": data.sentiment,
            "score": data.score,
            "source": data.source,
            "source_id": data.source_id,
            "created_at": datetime.now(timezone.utc),
        }

        result = await self.collection.insert_one(doc)
        doc["_id"] = result.inserted_id

        return self._doc_to_model(doc)

    async def create_batch(
        self, records: List[SentimentCreate]
    ) -> BatchCreateResult:
        """Create multiple sentiment records with deduplication.

        Records with a source_id that already exists for the same source
        will be skipped. Records without source_id are always created.

        Args:
            records: List of sentiment records to create.

        Returns:
            Result with created and skipped counts.
        """
        # Separate records with and without source_id
        records_with_id = [r for r in records if r.source_id]
        records_without_id = [r for r in records if not r.source_id]

        skipped_count = 0
        to_insert = []

        # Check for existing source_ids to avoid duplicates
        if records_with_id:
            existing_ids = set()
            for record in records_with_id:
                existing = await self.collection.find_one(
                    {"source": record.source, "source_id": record.source_id}
                )
                if existing:
                    existing_ids.add((record.source, record.source_id))

            for record in records_with_id:
                if (record.source, record.source_id) in existing_ids:
                    skipped_count += 1
                else:
                    to_insert.append(record)

        # Add records without source_id (always create)
        to_insert.extend(records_without_id)

        created_count = 0
        if to_insert:
            now = datetime.now(timezone.utc)
            docs = [
                {
                    "text": r.text,
                    "sentiment": r.sentiment,
                    "score": r.score,
                    "source": r.source,
                    "source_id": r.source_id,
                    "created_at": now,
                }
                for r in to_insert
            ]
            result = await self.collection.insert_many(docs)
            created_count = len(result.inserted_ids)

        return BatchCreateResult(
            created_count=created_count,
            skipped_count=skipped_count,
        )

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
