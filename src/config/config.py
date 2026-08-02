from configparser import ConfigParser
from typing import Any, List

from settings import ROOT_DIR
from src.config.env_interpolation import EnvInterpolation


class Config:
    @classmethod
    def get_instance(cls: Any) -> Any:
        if not getattr(cls, "_instance", None):
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        config_parser: ConfigParser = ConfigParser(
            interpolation=EnvInterpolation()
        )  # noqa E501
        config_parser.read(f"{ROOT_DIR}/resources/config.ini")
        self.db_configs: Config.DatabaseConfig = Config.DatabaseConfig(
            config_parser
        )  # noqa E501
        self.project_config: Config.ProjectConfig = Config.ProjectConfig(
            config_parser
        )  # noqa E501
        self.server_config: Config.ServerConfig = Config.ServerConfig(
            config_parser
        )  # noqa E501

    class DatabaseConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.db_url: str = configs.get("Database", "DB_URL")
            if not self.db_url:
                raise RuntimeError(
                    "Database is not configured: set the DB_URL environment "
                    "variable, e.g. "
                    "postgresql+psycopg2://user:pass@host:5432/auto_cart"
                )
            self.pool_size: int = configs.getint("Database", "POOL_SIZE")
            self.max_overflow: int = configs.getint(
                "Database", "MAX_OVERFLOW"
            )  # noqa E501
            self.pool_timeout: int = configs.getint(
                "Database", "POOL_TIMEOUT"
            )  # noqa E501

    class ProjectConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.name: str = configs.get("Project", "NAME")
            self.api: str = configs.get("Project", "API")
            self.version: str = configs.get("Project", "VERSION")

    class ServerConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.enable_docs: bool = configs.getboolean(
                "Server", "ENABLE_DOCS"
            )  # noqa E501
            self.cors_origins: List[str] = [
                origin.strip()
                for origin in configs.get("Server", "CORS_ORIGINS").split(",")
                if origin.strip()
            ]
            self.rate_limit: str = configs.get("Server", "RATE_LIMIT")
            self.max_request_bytes: int = configs.getint(
                "Server", "MAX_REQUEST_BYTES"
            )  # noqa E501
            self.sentry_dsn: str = configs.get("Server", "SENTRY_DSN")
            self.log_level: str = configs.get("Server", "LOG_LEVEL")
