"""
Database configuration and session management utilities.

This module contains the database setup, including the creation of the database engine,
session configuration, and the base class for SQLAlchemy models. It also includes a dependency
to manage database sessions, ensuring that sessions are created, used, and closed properly
within the application.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from foundever.core import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    url=DATABASE_URL,
    pool_size=5,
    max_overflow=10,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency to get a database session.
    Yields:
        SessionLocal: A new database session.
    Closes the session after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
