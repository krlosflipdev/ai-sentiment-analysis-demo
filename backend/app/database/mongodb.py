"""MongoDB connection management using Motor async driver."""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings


class MongoDB:
    """MongoDB connection wrapper.

    Holds the Motor client and database instances for the application.

    Attributes:
        client: The Motor async client instance.
        db: The database instance.
    """

    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


mongodb = MongoDB()


async def connect_to_mongodb() -> None:
    """Initialize MongoDB connection on application startup.

    Creates the Motor client and selects the database specified in settings.
    """
    mongodb.client = AsyncIOMotorClient(settings.mongodb_uri)
    mongodb.db = mongodb.client[settings.database_name]


async def close_mongodb_connection() -> None:
    """Close MongoDB connection on application shutdown.

    Properly closes the Motor client to release resources.
    """
    if mongodb.client:
        mongodb.client.close()


def get_database() -> AsyncIOMotorDatabase:
    """FastAPI dependency to get the database instance.

    Returns:
        The MongoDB database instance.

    Raises:
        RuntimeError: If database is not initialized.
    """
    if mongodb.db is None:
        raise RuntimeError("Database not initialized")
    return mongodb.db
