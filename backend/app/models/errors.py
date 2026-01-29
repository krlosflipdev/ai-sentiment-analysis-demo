"""Error response models for consistent error formatting."""

from typing import List, Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Details about a specific validation or field error.

    Attributes:
        field: The field that caused the error (if applicable).
        message: Description of the error.
    """

    field: Optional[str] = Field(None, description="Field name if applicable")
    message: str = Field(..., description="Error description")


class ErrorResponse(BaseModel):
    """Structured error response.

    Attributes:
        code: Machine-readable error code (e.g., NOT_FOUND, VALIDATION_ERROR).
        message: Human-readable error message.
        details: Additional error details for validation errors.
    """

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: List[ErrorDetail] = Field(
        default_factory=list, description="Additional error details"
    )


class APIErrorBody(BaseModel):
    """Wrapper for error responses.

    Attributes:
        error: The error response object.
    """

    error: ErrorResponse
