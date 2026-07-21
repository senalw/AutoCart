import logging
from typing import Dict

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from src.core.container import Container
from src.core.database.postgres_client import PostgresClient
from src.core.rate_limit import limiter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", include_in_schema=False)
@limiter.exempt
async def health() -> Dict[str, str]:
    """Liveness: the process is up and serving requests."""
    return {"status": "ok"}


@router.get("/ready", include_in_schema=False)
@limiter.exempt
@inject
async def ready(
    response: Response,
    db: PostgresClient = Depends(Provide[Container.db]),  # noqa B008
) -> Dict[str, str]:
    """Readiness: the instance can reach its database."""
    try:
        with db.db_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        logger.exception("readiness check failed")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unavailable"}
    return {"status": "ok"}
