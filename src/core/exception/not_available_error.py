from fastapi import status
from src.core.exception import AutoCartServiceError


class NotAvailableError(AutoCartServiceError):
    def __init__(self, message: str, code: status = status.HTTP_410_GONE) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Not Available: {self.message}"
