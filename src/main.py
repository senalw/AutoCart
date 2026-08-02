from contextlib import asynccontextmanager
from typing import AsyncIterator

import sentry_sdk
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.api.health import router as health_router
from src.api.v1.routes import routers as v1_routers
from src.core.container import Container
from src.core.logging_config import configure_logging
from src.core.middleware import (
    BodySizeLimitMiddleware,
    RequestContextMiddleware,
)
from src.core.rate_limit import limiter
from src.util.singleton import singleton
from starlette.middleware.cors import CORSMiddleware


@singleton
class AppCreator:
    def __init__(self) -> None:
        server_config = Container.conf.server_config

        configure_logging(server_config.log_level)

        if server_config.sentry_dsn:
            sentry_sdk.init(
                dsn=server_config.sentry_dsn,
                release=Container.conf.project_config.version,
                traces_sample_rate=0.1,
            )

        # set db and container
        self.container = Container()
        self.db = self.container.db()

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncIterator[None]:
            yield
            # uvicorn has drained in-flight requests by now (SIGTERM);
            # release the connection pool before the process exits
            self.db.close()

        # set app default; docs and schema are only served when enabled
        api_prefix = Container.conf.project_config.api
        self.app = FastAPI(
            title=Container.conf.project_config.name,
            openapi_url=(
                f"{api_prefix}/openapi.json" if server_config.enable_docs else None
            ),
            docs_url="/docs" if server_config.enable_docs else None,
            redoc_url="/redoc" if server_config.enable_docs else None,
            version=Container.conf.project_config.version,
            swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
            lifespan=lifespan,
        )

        # BELOW SECTION ADDED FOR TESTING PURPOSE #
        # table creation can be done using flyway
        self.db.drop_tables()
        self.db.create_tables()

        # insert same data
        self.db.insert_sample_data()
        #######################################################

        # rate limiting (per-client-ip default limit on all routes)
        self.app.state.limiter = limiter
        self.app.add_exception_handler(
            RateLimitExceeded, _rate_limit_exceeded_handler
        )  # noqa E501
        self.app.add_middleware(SlowAPIMiddleware)

        self.app.add_middleware(
            BodySizeLimitMiddleware,
            max_bytes=server_config.max_request_bytes,
        )

        # explicit cross-origin policy: nothing allowed unless configured
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=server_config.cors_origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # outermost: request id + access logging wraps everything above
        self.app.add_middleware(RequestContextMiddleware)

        Instrumentator(excluded_handlers=["/metrics", "/health", "/ready"]).instrument(
            self.app
        ).expose(self.app, include_in_schema=False)

        self.app.include_router(health_router)
        self.app.include_router(v1_routers, prefix="/api/v1")


app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
container = app_creator.container
