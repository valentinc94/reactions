"""
Test configuration for database and background tasks.

This module contains utility classes and fixtures to manage the test database configuration
and background tasks for unit tests. It includes setup and teardown of the test database,
as well as the provision of a session for database interactions and a BackgroundTasks instance for testing.
"""

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from reactions.core import database
from reactions.interfaces import routes


class TestDatabase:
    """A utility class to manage the test database configuration."""

    def __init__(self, database_url: str = "sqlite:///:memory:"):
        self.engine: Engine = create_engine(
            database_url, connect_args={"check_same_thread": False}
        )
        self.connection = self.engine.connect()
        self.session_local = sessionmaker(bind=self.connection)

    def setup(self):
        """Set up the database tables."""
        database.Base.metadata.create_all(bind=self.connection)

    def teardown(self):
        """Tear down the database tables."""
        database.Base.metadata.drop_all(bind=self.connection)

    def get_session(self) -> Session:
        """Return a database session."""
        return self.session_local()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Fixture to manage a test database session."""
    test_db = TestDatabase()
    test_db.setup()
    session = test_db.get_session()

    try:
        yield session
    finally:
        session.close()
        test_db.teardown()


@pytest.fixture(scope="function")
def client(
    db_session: Session,  # pylint: disable=redefined-outer-name
) -> Generator[TestClient, None, None]:
    """
    Provides a TestClient for the FastAPI app with overridden dependencies.

    Overrides the database session and background tasks for testing purposes.

    Args:
        db_session (Session): Database session for the test.
        background_tasks (BackgroundTasks): Background tasks for the test.
        worker_manager (workers.WorkerManager): Handles background task orchestration.

    Yields:
        TestClient: Configured TestClient for the app.
    """

    routes.app.dependency_overrides[database.get_db] = lambda: db_session

    with TestClient(routes.app) as test_client:
        yield test_client

    routes.app.dependency_overrides.clear()
