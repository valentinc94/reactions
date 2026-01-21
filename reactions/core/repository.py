"""
Database utility functions for handling model instances.

This module provides utility functions for common database operations, such as creating
and updating model instances. It includes methods to save new instances, update existing ones,
and ensure proper transaction handling and instance refreshing within the SQLAlchemy session.
"""

from sqlalchemy.orm import Session

from reactions.core import types


def create(db: Session, instance: types.Instance) -> types.Instance:
    """
    Create a new instance in the database, commit the transaction, and refresh the instance.

    Args:
        db (Session): SQLAlchemy session object.
        instance (Instance): The SQLAlchemy model instance to save.

    Returns:
        The saved instance.
    """
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update(db: Session, instance: types.Instance) -> types.Instance:
    """
    Update an existing instance in the database, commit the transaction, and refresh the instance.

    Args:
        db (Session): SQLAlchemy session object.
        instance (Instance): The SQLAlchemy model instance to save.

    Returns:
        T: The updated instance.
    """
    db.commit()
    db.refresh(instance)
    return instance


def delete(db: Session, instance: types.Instance) -> None:
    """
    Delete an existing instance from the database and commit the transaction.

    Args:
        db (Session): SQLAlchemy session object.
        instance (Instance): The SQLAlchemy model instance to delete.
    """
    db.delete(instance)
    db.commit()
