"""Custom exception classes and handlers."""

from app.exceptions.handlers import (
    APIException,
    NotFoundError,
    ValidationError,
    api_exception_handler,
)

__all__ = [
    "APIException",
    "NotFoundError",
    "ValidationError",
    "api_exception_handler",
]
