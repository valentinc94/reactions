"""
Business logic and process handling for the Users module.

This module contains the core business processes for managing users
"""

from typing import List

from sqlalchemy.orm import Session

from reactions.apps.users import models
from reactions.core import repository
from reactions.domains.users import exceptions, queries, schemas, validations


def create_user(
    db: Session,
    user_data: schemas.UserCreate,
) -> models.User:
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user_data (schemas.UserCreate): Data required to create a user.

    Returns:
        models.User: The created user instance.

    Raises:
        exceptions.UsernameAlreadyExists: If the username is already taken.
    """

    if validations.check_if_username_exists(db=db, username=user_data.username):
        raise exceptions.UsernameAlreadyExists(username=user_data.username)

    instance = models.User.new(
        username=user_data.username,
        reactions=user_data.reactions.model_dump(),
        role=user_data.role,
        last_reaction_at=user_data.last_reaction_at,
    )

    repository.create(db=db, instance=instance)

    return instance


def update_user(
    db: Session,
    user_data: schemas.UserUpdate,
) -> models.User:
    """
    Update a  user in the database.

    Args:
        db (Session): Database session.
        user_data (schemas.UserUpdate): Data required to update a user.

    Returns:
        models.User: The user instance.

    Raises:
        exceptions.UserDoesNotExist: If the username does not exists.
    """

    if not validations.check_if_username_exists(db=db, username=user_data.username):
        raise exceptions.UserDoesNotExist()

    user = queries.fetch_user_record_by_username(db=db, username=user_data.username)

    user.role = user_data.role or user.role
    user.last_reaction_at = user_data.last_reaction_at or user.last_reaction_at

    if user_data.reactions:
        user.reactions = user_data.reactions.model_dump()

    instance = repository.update(db=db, instance=user)
    return instance


def delete_user(
    db: Session,
    username: str,
) -> None:
    """
    Update a  user in the database.

    Args:
        db (Session): Database session.
        username (str): the username to delete.

    Returns:
        None

    Raises:
        exceptions.UserDoesNotExist: If the username does not exists.
    """
    # TODO: is_disabled for remove users, no apply on this assignment

    if not validations.check_if_username_exists(db=db, username=username):
        raise exceptions.UserDoesNotExist()

    user = queries.fetch_user_record_by_username(db=db, username=username)

    repository.delete(db=db, instance=user)


def retrieve_users(
    db: Session,
    username: str | None = None,
) -> List[schemas.UserRetrieve]:
    """
    Retrieve users from the database, optionally filtered by username.

    Args:
        db (Session): SQLAlchemy database session.
        username (str | None): Optional username to filter users.

    Returns:
        List[schemas.UserRetrieve]: A list of users with their public attributes,
        including id, username, role, reactions, last reaction timestamp,
        creation timestamp, and last update timestamp.
    """

    users = queries.fetch_users(db=db, username=username)

    return [
        schemas.UserRetrieve(
            id=user.id,
            username=user.username,
            role=user.role,
            reactions=user.reactions,
            last_reaction_at=str(user.last_reaction_at),
            created_at=str(user.created_at),
            updated_at=str(user.updated_at),
        )
        for user in users
    ]
