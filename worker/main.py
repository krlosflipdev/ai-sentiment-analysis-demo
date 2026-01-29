"""Worker CLI entry point."""

import argparse
import asyncio
import logging
import sys

from worker.config import settings
from worker.pipeline import Pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Sentiment Analysis Worker",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-k",
        "--keyword",
        type=str,
        default=settings.default_keyword,
        help="Search keyword for fetching posts",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=settings.default_limit,
        help="Maximum posts to fetch per source",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without saving to API",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()


async def main() -> int:
    """Main worker entry point.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("=" * 50)
    logger.info("Sentiment Analysis Worker")
    logger.info("=" * 50)
    logger.info(f"Keyword: {args.keyword}")
    logger.info(f"Limit: {args.limit}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info(f"API URL: {settings.api_base_url}")
    logger.info("=" * 50)

    pipeline = Pipeline(dry_run=args.dry_run)

    try:
        await pipeline.initialize()
        result = await pipeline.run(args.keyword, args.limit)

        logger.info("=" * 50)
        logger.info("Summary")
        logger.info("=" * 50)
        logger.info(f"Posts fetched: {result.fetched}")
        logger.info(f"Posts analyzed: {result.analyzed}")
        logger.info(f"Records created: {result.created}")
        logger.info(f"Duplicates skipped: {result.skipped}")
        logger.info("=" * 50)

        return 0

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        return 1

    finally:
        await pipeline.close()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
