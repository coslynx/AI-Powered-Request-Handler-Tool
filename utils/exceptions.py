from fastapi import HTTPException, status
from typing import Optional, Union

class APIError(HTTPException):
    """Custom exception class for API-related errors."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST, headers: Optional[dict] = None):
        super().__init__(detail=detail, status_code=status_code, headers=headers)

class NotFoundError(APIError):
    """Custom exception class for not found errors."""
    def __init__(self, detail: str = "Resource not found.", status_code: int = status.HTTP_404_NOT_FOUND, headers: Optional[dict] = None):
        super().__init__(detail=detail, status_code=status_code, headers=headers)

class DatabaseError(APIError):
    """Custom exception class for database-related errors."""
    def __init__(self, detail: str = "Database error occurred.", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, headers: Optional[dict] = None):
        super().__init__(detail=detail, status_code=status_code, headers=headers)

class ValidationException(APIError):
    """Custom exception class for validation errors."""
    def __init__(self, detail: Union[str, list], status_code: int = status.HTTP_400_BAD_REQUEST, headers: Optional[dict] = None):
        super().__init__(detail=detail, status_code=status_code, headers=headers)

class OpenAIAPIError(APIError):
    """Custom exception class for errors related to the OpenAI API."""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, headers: Optional[dict] = None):
        super().__init__(detail=detail, status_code=status_code, headers=headers)