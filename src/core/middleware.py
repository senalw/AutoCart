import logging
import time
import uuid

from src.core.logging_config import request_id_ctx
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

access_logger = logging.getLogger("autocart.access")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Assigns each request an id, logs its completion, and returns the
    id in the X-Request-ID response header for cross-system tracing."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        token = request_id_ctx.set(request_id)
        start = time.perf_counter()
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            access_logger.info(
                "request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(
                        (time.perf_counter() - start) * 1000, 2
                    ),  # noqa E501
                },
            )
            return response
        except Exception:
            access_logger.exception(
                "request failed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": round(
                        (time.perf_counter() - start) * 1000, 2
                    ),  # noqa E501
                },
            )
            raise
        finally:
            request_id_ctx.reset(token)


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    """Rejects requests whose declared body size exceeds the limit."""

    def __init__(self, app: ASGIApp, max_bytes: int) -> None:
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                declared_size = int(content_length)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid Content-Length header"},
                )
            if declared_size > self.max_bytes:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request body too large"},
                )
        return await call_next(request)
