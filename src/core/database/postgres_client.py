import logging
from contextlib import contextmanager

from fastapi import status
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.exc import DataError, IntegrityError, OperationalError, ProgrammingError
from sqlalchemy.orm import Session, sessionmaker
from src.config.config import Config
from src.core.exception import (
    AutoCartServiceError,
    ConstraintViolationError,
    DatabaseConnectionError,
    InvalidArgumentError,
)
from src.domain.entity.base import Base


class PostgresClient:
    def __init__(self, configs: Config.DatabaseConfig) -> None:
        self.db_engine: Engine = create_engine(
            configs.db_url,
            pool_size=configs.pool_size,
            max_overflow=configs.max_overflow,
            pool_timeout=configs.pool_timeout,
            # detect stale connections (e.g. after a db restart) before use
            pool_pre_ping=True,
        )
        # "auto flush" should be turned off for merging objects in a same session.
        self.session_maker = sessionmaker(bind=self.db_engine, autoflush=False)

    @contextmanager
    def get_session(self) -> Session:
        session = None
        try:
            session = self.session_maker()
            yield session
            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            self._handle_db_errors(e)
        finally:
            if session:
                session.flush()
                session.close()

    def close(self) -> None:
        # release all pooled connections; called on app shutdown
        self.db_engine.dispose()

    def drop_tables(self) -> None:
        Base.metadata.drop_all(self.db_engine)

    def create_tables(self) -> None:
        Base.metadata.create_all(self.db_engine)

    def insert_sample_data(self) -> None:
        for table in ["products"]:
            with open(f"resources/sample_data/{table}.sql", "r") as sql_file:
                with self.get_session() as session:
                    for statement in sql_file:
                        session.execute(text(statement))

    @staticmethod
    def _handle_db_errors(throwable: Exception) -> None:
        logging.exception(throwable)

        if isinstance(throwable, AutoCartServiceError):
            raise throwable
        elif isinstance(
            throwable,
            DataError,
        ):  # passing None/Incorrect parameter for mandatory parameter
            raise InvalidArgumentError("Invalid argument")
        elif isinstance(throwable, AttributeError):
            # details are in the log above; don't echo internals to clients
            raise InvalidArgumentError("Invalid request data")
        elif isinstance(
            throwable, (OperationalError, ProgrammingError)
        ):  # Programming error occurs when table not found
            raise DatabaseConnectionError("Unable to connect to the database")
        elif isinstance(throwable, IntegrityError):  # db constraint error
            raise ConstraintViolationError("Unique key or Not null violation")
        else:
            raise AutoCartServiceError(
                "Unknown Error", status.HTTP_500_INTERNAL_SERVER_ERROR
            )
