"""Twitter/X API v2 data fetcher."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import List, Optional

import httpx

from worker.config import settings
from worker.fetcher.base import BaseFetcher, FetchedPost

logger = logging.getLogger(__name__)


class TwitterFetcher(BaseFetcher):
    """Fetcher for Twitter/X API v2.

    Uses the recent search endpoint to fetch tweets matching a keyword.
    Implements exponential backoff for rate limit handling.
    """

    BASE_URL = "https://api.twitter.com/2"

    def __init__(self, bearer_token: Optional[str] = None):
        """Initialize the Twitter fetcher.

        Args:
            bearer_token: Twitter API bearer token. Defaults to settings.
        """
        self._token = bearer_token or settings.twitter_bearer_token
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def source_name(self) -> str:
        """Return the source identifier."""
        return "twitter"

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                headers={
                    "Authorization": f"Bearer {self._token}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
        return self._client

    async def health_check(self) -> bool:
        """Verify Twitter API connectivity.

        Returns:
            True if authenticated and ready, False otherwise.
        """
        if not self._token:
            logger.warning("Twitter: No bearer token configured")
            return False

        try:
            client = await self._get_client()
            # Use a simple endpoint to verify auth
            response = await client.get(
                "/tweets/search/recent",
                params={"query": "test", "max_results": 10},
            )
            if response.status_code == 200:
                logger.info("Twitter: Health check passed")
                return True
            elif response.status_code == 401:
                logger.error("Twitter: Invalid bearer token")
                return False
            elif response.status_code == 429:
                logger.warning("Twitter: Rate limited during health check")
                return True  # API is accessible, just rate limited
            else:
                logger.error(f"Twitter: Unexpected status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Twitter: Health check failed - {e}")
            return False

    async def fetch(self, keyword: str, limit: int = 100) -> List[FetchedPost]:
        """Fetch tweets matching the keyword.

        Args:
            keyword: Search keyword.
            limit: Maximum number of tweets to fetch (max 100 per request).

        Returns:
            List of fetched tweets in standardized format.
        """
        if not self._token:
            logger.warning("Twitter: No bearer token, skipping fetch")
            return []

        client = await self._get_client()
        posts: List[FetchedPost] = []

        # Twitter API max_results is 10-100
        max_results = min(limit, 100)

        params = {
            "query": f"{keyword} -is:retweet lang:en",
            "max_results": max_results,
            "tweet.fields": "created_at,author_id,text",
            "expansions": "author_id",
            "user.fields": "username",
        }

        for attempt in range(3):
            try:
                response = await client.get("/tweets/search/recent", params=params)

                if response.status_code == 429:
                    # Rate limited - exponential backoff
                    wait_time = (2**attempt) * 5
                    logger.warning(f"Twitter: Rate limited, waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()

                if "data" not in data:
                    logger.info("Twitter: No tweets found")
                    return []

                # Build user lookup
                users = {}
                if "includes" in data and "users" in data["includes"]:
                    for user in data["includes"]["users"]:
                        users[user["id"]] = user["username"]

                for tweet in data["data"]:
                    posts.append(
                        FetchedPost(
                            source_id=tweet["id"],
                            text=tweet["text"],
                            source=self.source_name,
                            author=users.get(tweet["author_id"], "unknown"),
                            created_at=tweet.get(
                                "created_at",
                                datetime.now(timezone.utc).isoformat(),
                            ),
                        )
                    )

                logger.info(f"Twitter: Fetched {len(posts)} tweets")
                return posts

            except httpx.HTTPStatusError as e:
                logger.error(f"Twitter: HTTP error {e.response.status_code}")
                if attempt < 2:
                    await asyncio.sleep(2**attempt)
                continue
            except Exception as e:
                logger.error(f"Twitter: Fetch error - {e}")
                break

        return posts

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
