"""Main sentiment analysis pipeline orchestrator."""

import logging
from dataclasses import dataclass
from typing import List, Optional

from worker.analyzer import AnalysisResult, SentimentAnalyzer
from worker.config import settings
from worker.fetcher import BaseFetcher, FetchedPost, RedditFetcher, TwitterFetcher
from worker.storage import APIClient

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Result summary from a pipeline run.

    Attributes:
        fetched: Total posts fetched from all sources.
        analyzed: Total posts analyzed.
        created: New records created in the database.
        skipped: Duplicate records skipped.
    """

    fetched: int = 0
    analyzed: int = 0
    created: int = 0
    skipped: int = 0


class Pipeline:
    """Main sentiment analysis pipeline orchestrator.

    Coordinates data fetching, sentiment analysis, and result storage.
    Supports multiple data sources with automatic fallback.
    """

    def __init__(self, dry_run: bool = False):
        """Initialize the pipeline.

        Args:
            dry_run: If True, don't save results to API.
        """
        self._dry_run = dry_run
        self._analyzer: Optional[SentimentAnalyzer] = None
        self._api_client: Optional[APIClient] = None
        self._fetchers: List[BaseFetcher] = []
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize pipeline components with health checks.

        Raises:
            RuntimeError: If no data fetchers are available.
        """
        if self._initialized:
            return

        logger.info("Initializing pipeline...")

        # Initialize sentiment analyzer
        self._analyzer = SentimentAnalyzer()

        # Initialize API client
        if not self._dry_run:
            self._api_client = APIClient()
            if not await self._api_client.health_check():
                raise RuntimeError("Backend API is not accessible")

        # Initialize fetchers with health checks
        twitter = TwitterFetcher()
        if await twitter.health_check():
            self._fetchers.append(twitter)
            logger.info("Twitter fetcher enabled")

        reddit = RedditFetcher()
        if await reddit.health_check():
            self._fetchers.append(reddit)
            logger.info("Reddit fetcher enabled")

        if not self._fetchers:
            raise RuntimeError(
                "No data fetchers available. "
                "Configure TWITTER_BEARER_TOKEN or check internet connectivity."
            )

        self._initialized = True
        logger.info(f"Pipeline initialized with {len(self._fetchers)} fetcher(s)")

    async def run(self, keyword: str, limit: int = 100) -> PipelineResult:
        """Run the full sentiment analysis pipeline.

        Args:
            keyword: Search keyword for fetching posts.
            limit: Maximum posts to fetch per source.

        Returns:
            PipelineResult with counts.

        Raises:
            RuntimeError: If pipeline is not initialized.
        """
        if not self._initialized:
            await self.initialize()

        logger.info(f"Starting pipeline for keyword: '{keyword}' (limit: {limit})")
        result = PipelineResult()

        # Fetch from all available sources
        all_posts: List[FetchedPost] = []
        for fetcher in self._fetchers:
            try:
                posts = await fetcher.fetch(keyword, limit)
                all_posts.extend(posts)
                logger.info(
                    f"Fetched {len(posts)} posts from {fetcher.source_name}"
                )
            except Exception as e:
                logger.error(f"Error fetching from {fetcher.source_name}: {e}")

        result.fetched = len(all_posts)

        if not all_posts:
            logger.warning("No posts fetched from any source")
            return result

        # Analyze sentiment
        texts = [p.text for p in all_posts]
        analysis_results: List[AnalysisResult] = self._analyzer.analyze_batch(texts)
        result.analyzed = len(analysis_results)

        logger.info(f"Analyzed {result.analyzed} posts")

        # Log sentiment distribution
        positive = sum(1 for r in analysis_results if r.label == "positive")
        negative = sum(1 for r in analysis_results if r.label == "negative")
        neutral = sum(1 for r in analysis_results if r.label == "neutral")
        logger.info(
            f"Sentiment distribution: {positive} positive, "
            f"{negative} negative, {neutral} neutral"
        )

        # Save results
        if self._dry_run:
            logger.info("Dry run - skipping save to API")
            result.created = result.analyzed
        else:
            try:
                save_result = await self._api_client.save_batch(
                    all_posts, analysis_results
                )
                result.created = save_result["created_count"]
                result.skipped = save_result["skipped_count"]
            except Exception as e:
                logger.error(f"Error saving results: {e}")
                raise

        logger.info(
            f"Pipeline complete: {result.fetched} fetched, "
            f"{result.analyzed} analyzed, {result.created} created, "
            f"{result.skipped} skipped"
        )

        return result

    async def close(self) -> None:
        """Clean up pipeline resources."""
        for fetcher in self._fetchers:
            await fetcher.close()

        if self._api_client:
            await self._api_client.close()
