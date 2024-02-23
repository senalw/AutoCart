from fastapi import FastAPI
from src.api.v1.routes import routers as v1_routers
from src.core.container import Container
from src.util.singleton import singleton


@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=Container.conf.project_config.name,
            openapi_url=f"{Container.conf.project_config.api}/openapi.json",
            version=Container.conf.project_config.version,
            swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        )

        # set db and container
        self.container = Container()
        self.db = self.container.db()
        self.db.drop_tables()
        self.db.create_tables()

        # Route to serve the Swagger UI
        @self.app.get("/docs", include_in_schema=False)
        async def custom_swagger_ui_html():
            return app.openapi_html()

        # Route to serve the OpenAPI schema
        @self.app.get("/openapi.json", include_in_schema=False)
        async def get_openapi():
            return app.openapi()

        self.app.include_router(v1_routers, prefix="/api/v1")


app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
container = app_creator.container
