"""Base fetcher interface and data models."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class FetchedPost:
    """Standardized post format from any data source.

    Attributes:
        source_id: Unique identifier from the platform.
        text: Post content/text.
        source: Data source name (e.g., 'twitter', 'reddit').
        author: Username of the post author.
        created_at: ISO timestamp when the post was created.
    """

    source_id: str
    text: str
    source: str
    author: str
    created_at: str


class BaseFetcher(ABC):
    """Abstract base class for data fetchers.

    All fetchers must implement fetch() and health_check() methods.
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the source identifier (e.g., 'twitter', 'reddit')."""
        pass

    @abstractmethod
    async def fetch(self, keyword: str, limit: int = 100) -> List[FetchedPost]:
        """Fetch posts matching the keyword.

        Args:
            keyword: Search keyword.
            limit: Maximum number of posts to fetch.

        Returns:
            List of fetched posts in standardized format.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify API connectivity and authentication.

        Returns:
            True if the fetcher is ready to use, False otherwise.
        """
        pass
