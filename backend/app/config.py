"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        mongodb_uri: MongoDB connection string.
        database_name: Name of the MongoDB database.
        api_host: Host address for the API server.
        api_port: Port number for the API server.
        default_page_size: Default number of items per page.
        max_page_size: Maximum allowed items per page.
    """

    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "sentiment"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    default_page_size: int = 20
    max_page_size: int = 100

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        extra = "ignore"


settings = Settings()
