"""HTTP client for posting results to the backend API."""

import logging
from typing import Any, Dict, List

import httpx

from worker.analyzer.sentiment import AnalysisResult
from worker.config import settings
from worker.fetcher.base import FetchedPost

logger = logging.getLogger(__name__)


class APIClient:
    """HTTP client for posting sentiment results to the backend API.

    Uses the batch endpoint for efficient bulk inserts with
    automatic deduplication by source_id.
    """

    def __init__(self, base_url: str = ""):
        """Initialize the API client.

        Args:
            base_url: Backend API base URL. Defaults to settings.api_base_url.
        """
        self._base_url = base_url or settings.api_base_url
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={"Content-Type": "application/json"},
            timeout=60.0,
        )

    async def health_check(self) -> bool:
        """Verify backend API connectivity.

        Returns:
            True if API is accessible, False otherwise.
        """
        try:
            response = await self._client.get("/api/v1/health")
            if response.status_code == 200:
                logger.info("API: Health check passed")
                return True
            else:
                logger.error(f"API: Health check failed - status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"API: Health check failed - {e}")
            return False

    async def save_single(
        self, post: FetchedPost, result: AnalysisResult
    ) -> Dict[str, Any]:
        """Save a single sentiment record.

        Args:
            post: The fetched post data.
            result: The analysis result.

        Returns:
            Created record data from the API.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        payload = {
            "text": post.text,
            "sentiment": result.label,
            "score": result.score,
            "source": post.source,
            "source_id": post.source_id,
        }

        response = await self._client.post("/api/v1/sentiments", json=payload)
        response.raise_for_status()
        return response.json()["data"]

    async def save_batch(
        self, posts: List[FetchedPost], results: List[AnalysisResult]
    ) -> Dict[str, int]:
        """Save multiple sentiment records with deduplication.

        Args:
            posts: List of fetched posts.
            results: List of analysis results (same order as posts).

        Returns:
            Dict with 'created_count' and 'skipped_count'.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        if len(posts) != len(results):
            raise ValueError("Posts and results must have the same length")

        if not posts:
            return {"created_count": 0, "skipped_count": 0}

        records = [
            {
                "text": post.text,
                "sentiment": result.label,
                "score": result.score,
                "source": post.source,
                "source_id": post.source_id,
            }
            for post, result in zip(posts, results)
        ]

        logger.info(f"API: Saving batch of {len(records)} records")

        response = await self._client.post(
            "/api/v1/sentiments/batch",
            json={"records": records},
        )
        response.raise_for_status()

        data = response.json()["data"]
        logger.info(
            f"API: Created {data['created_count']}, "
            f"skipped {data['skipped_count']} duplicates"
        )
        return data

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
