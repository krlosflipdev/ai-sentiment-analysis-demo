"""Worker configuration settings."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Worker configuration loaded from environment variables.

    Attributes:
        mongodb_uri: MongoDB connection string.
        twitter_bearer_token: Twitter API v2 bearer token.
        huggingface_api_key: HuggingFace API key (optional).
        api_base_url: Backend API base URL.
        default_keyword: Default search keyword.
        default_limit: Default number of posts to fetch.
    """

    mongodb_uri: str = os.getenv("MONGODB_URI", "")
    twitter_bearer_token: str = os.getenv("TWITTER_BEARER_TOKEN", "")
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")
    api_base_url: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    default_keyword: str = os.getenv("DEFAULT_KEYWORD", "AI")
    default_limit: int = int(os.getenv("DEFAULT_LIMIT", "100"))


settings = Settings()
