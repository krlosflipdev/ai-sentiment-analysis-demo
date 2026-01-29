"""Custom exception classes and FastAPI exception handlers."""

from typing import List, Optional

from fastapi import Request
from fastapi.responses import JSONResponse

from app.models.errors import ErrorDetail


class APIException(Exception):
    """Base exception for API errors.

    Args:
        code: Machine-readable error code.
        message: Human-readable error message.
        status_code: HTTP status code.
        details: List of additional error details.
    """

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[List[ErrorDetail]] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


class NotFoundError(APIException):
    """Exception raised when a resource is not found.

    Args:
        resource: Type of resource (e.g., "Sentiment").
        resource_id: ID of the resource that was not found.
    """

    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource} with id '{resource_id}' not found",
            status_code=404,
        )


class ValidationError(APIException):
    """Exception raised for validation errors.

    Args:
        message: Description of the validation error.
        details: List of field-level error details.
    """

    def __init__(self, message: str, details: Optional[List[ErrorDetail]] = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details,
        )


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """FastAPI exception handler for APIException.

    Args:
        request: The incoming request.
        exc: The raised APIException.

    Returns:
        JSON response with error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": [
                    {"field": d.field, "message": d.message} for d in exc.details
                ],
            }
        },
    )
