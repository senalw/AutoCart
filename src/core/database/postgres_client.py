import logging
from contextlib import contextmanager

from fastapi import status
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import DataError, IntegrityError, OperationalError, ProgrammingError
from sqlalchemy.orm import Session, sessionmaker

from src.config.config import Config
from src.core.exception import (
    ConstraintViolationError,
    DatabaseConnectionError,
    InvalidArgumentError,
    AutoCartServiceError,
)
from src.domain.entity.base import Base


class PostgresClient:
    def __init__(self, configs: Config.DatabaseConfig) -> None:
        self.db_engine: Engine = create_engine(configs.db_url)

    @contextmanager
    def get_session(self) -> Session:
        session = None
        try:
            # "auto flush" should be turned off for merging objects in a same session.
            sm = sessionmaker(bind=self.db_engine, autoflush=False)
            session = sm()
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

    def drop_tables(self):
        Base.metadata.drop_all(self.db_engine)

    def create_tables(self):
        Base.metadata.create_all(self.db_engine)

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
            raise InvalidArgumentError(f"Invalid attribute: [{throwable.name}]")
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
