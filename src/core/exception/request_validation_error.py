from fastapi import status
from src.core.exception import AutoCartServiceError


class RequestValidationError(AutoCartServiceError):
    def __init__(
        self, message: str, code: status = status.HTTP_400_BAD_REQUEST
    ) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Validation Error: {self.message}"
