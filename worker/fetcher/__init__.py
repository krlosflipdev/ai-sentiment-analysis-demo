"""Data fetcher modules."""

from worker.fetcher.base import BaseFetcher, FetchedPost
from worker.fetcher.reddit import RedditFetcher
from worker.fetcher.twitter import TwitterFetcher

__all__ = ["BaseFetcher", "FetchedPost", "TwitterFetcher", "RedditFetcher"]
