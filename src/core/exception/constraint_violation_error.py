from fastapi import status
from src.core.exception.auto_cart_service_error import AutoCartServiceError


class ConstraintViolationError(AutoCartServiceError):
    def __init__(
        self, message: str, code: status = status.HTTP_412_PRECONDITION_FAILED
    ) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Database constraint violation: {self.message}"
