import json
import logging
import sys
from contextvars import ContextVar
from typing import Optional

# request id of the request currently being handled, set by
# RequestContextMiddleware so every log line can be correlated
request_id_ctx: ContextVar[Optional[str]] = ContextVar(
    "request_id", default=None
)  # noqa E501

_EXTRA_FIELDS = ("method", "path", "status_code", "duration_ms")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        request_id = request_id_ctx.get()
        if request_id:
            log_entry["request_id"] = request_id
        for field in _EXTRA_FIELDS:
            if hasattr(record, field):
                log_entry[field] = getattr(record, field)
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, default=str)


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())

    # route uvicorn's own loggers through the json handler
    for name in ("uvicorn", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = True

    # RequestContextMiddleware emits access logs with request ids,
    # so uvicorn's plain-text access log is redundant
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers = []
    access_logger.propagate = False
