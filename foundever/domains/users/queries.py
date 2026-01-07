"""
Database query functions for the Users module.

This module contains functions that interact with the database to perform user-related queries.
It includes functions to retrieve, create, update, and delete user records, as well as handling
other database operations specific to user management, such as verifying credentials and managing
user roles and permissions.
"""

from typing import List

from sqlalchemy.orm import Session

from foundever.apps.users import models


def fetch_user_record_by_username(db: Session, username: str) -> models.User | None:
    """
    Check if a username already exists in the database
    and return the user record if found.

    Args:
        db (Session): SQLAlchemy database session.
        username (str): username/login to check (e.g., "valentinc94").

    Returns:
        models.User | None: The user record if it exists, None otherwise.
    """
    return (
        db.query(models.User).filter(models.User.username == username.lower()).first()
    )


def fetch_users(
    db: Session,
    username: str | None = None,
) -> List[models.User]:
    """
    Fetches users from the database

    Args:
        db (Session): The database session.
        username (str| None): Optional username associated with the user.

    Returns:
        List[models.Users]: A list of users instances matching the provided username.
    """

    query = db.query(models.User)

    if username:
        query = query.filter(models.User.username == username)

    return query.all()
