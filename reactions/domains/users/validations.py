"""
Validation functions for the Users module.

This module contains lightweight functions to validate user-related data
before creating, updating or querying users in the database.
"""

from sqlalchemy.orm import Session

from reactions.apps.users import models


def check_if_username_exists(db: Session, username: str) -> bool:
    """
    Check if a username already exists in the database.

    Args:
        db (Session): SQLAlchemy database session.
        username (str): username to check (e.g., "valentinc94").

    Returns:
        bool: True if the username already exists, False otherwise.
    """
    return (
        db.query(models.User).filter(models.User.username == username).first()
        is not None
    )
