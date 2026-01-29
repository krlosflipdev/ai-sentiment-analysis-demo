"""Reddit data fetcher using public JSON API."""

import logging
from datetime import datetime, timezone
from typing import List, Optional

import httpx

from worker.fetcher.base import BaseFetcher, FetchedPost

logger = logging.getLogger(__name__)


class RedditFetcher(BaseFetcher):
    """Fetcher for Reddit using public JSON API.

    Uses the public Reddit JSON API (no authentication required).
    Serves as a fallback when Twitter API is unavailable.
    """

    BASE_URL = "https://www.reddit.com"

    def __init__(self):
        """Initialize the Reddit fetcher."""
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def source_name(self) -> str:
        """Return the source identifier."""
        return "reddit"

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                headers={
                    # Reddit requires a User-Agent
                    "User-Agent": "SentimentAnalysisBot/1.0",
                },
                timeout=30.0,
                follow_redirects=True,
            )
        return self._client

    async def health_check(self) -> bool:
        """Verify Reddit API connectivity.

        Returns:
            True if accessible, False otherwise.
        """
        try:
            client = await self._get_client()
            response = await client.get("/r/all/new.json", params={"limit": 1})

            if response.status_code == 200:
                logger.info("Reddit: Health check passed")
                return True
            elif response.status_code == 429:
                logger.warning("Reddit: Rate limited during health check")
                return True  # API is accessible, just rate limited
            else:
                logger.error(f"Reddit: Unexpected status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Reddit: Health check failed - {e}")
            return False

    async def fetch(self, keyword: str, limit: int = 100) -> List[FetchedPost]:
        """Fetch Reddit posts matching the keyword.

        Args:
            keyword: Search keyword.
            limit: Maximum number of posts to fetch (max 100 per request).

        Returns:
            List of fetched posts in standardized format.
        """
        client = await self._get_client()
        posts: List[FetchedPost] = []

        # Reddit API limit is 100
        fetch_limit = min(limit, 100)

        try:
            response = await client.get(
                "/r/all/search.json",
                params={
                    "q": keyword,
                    "sort": "new",
                    "limit": fetch_limit,
                    "t": "day",  # Last 24 hours
                },
            )

            if response.status_code == 429:
                logger.warning("Reddit: Rate limited")
                return []

            response.raise_for_status()
            data = response.json()

            if "data" not in data or "children" not in data["data"]:
                logger.info("Reddit: No posts found")
                return []

            for item in data["data"]["children"]:
                post = item["data"]

                # Combine title and selftext for analysis
                text = post.get("title", "")
                selftext = post.get("selftext", "")
                if selftext and selftext != "[removed]":
                    text = f"{text}. {selftext}"

                # Skip very short posts or deleted content
                if len(text) < 10:
                    continue

                # Convert Unix timestamp to ISO format
                created_utc = post.get("created_utc", 0)
                created_at = datetime.fromtimestamp(
                    created_utc, tz=timezone.utc
                ).isoformat()

                posts.append(
                    FetchedPost(
                        source_id=post["id"],
                        text=text[:5000],  # Limit text length
                        source=self.source_name,
                        author=post.get("author", "[deleted]"),
                        created_at=created_at,
                    )
                )

            logger.info(f"Reddit: Fetched {len(posts)} posts")
            return posts

        except httpx.HTTPStatusError as e:
            logger.error(f"Reddit: HTTP error {e.response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Reddit: Fetch error - {e}")
            return []

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
