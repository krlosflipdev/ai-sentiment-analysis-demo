"""Base response models for consistent API responses."""

from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Pagination metadata for list responses.

    Attributes:
        page: Current page number (1-indexed).
        limit: Number of items per page.
        total: Total number of items across all pages.
        total_pages: Total number of pages.
    """

    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, description="Items per page")
    total: int = Field(..., ge=0, description="Total items")
    total_pages: int = Field(..., ge=0, description="Total pages")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper.

    Attributes:
        data: List of items for the current page.
        meta: Pagination metadata.
    """

    data: List[T]
    meta: PaginationMeta


class SingleResponse(BaseModel, Generic[T]):
    """Generic single item response wrapper.

    Attributes:
        data: The response data.
    """

    data: T
