"""
SQLAlchemy models for the Users module.

Defines the database structure for user-related entities.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from reactions.apps.users import constants
from reactions.core import database


class User(database.Base):
    """
    Represents a User in the database.
    Attributes:
        id (str): Unique identifier for the user (UUID).
        username (str): username (e.g., "valentinc94"). Must be unique.
        role (constants.Role): Classification of the user (e.g., EXTERNAL, INTERNAL, ADMIN).
        reactions (list[dict] | dict): Aggregated reaction counts given by the user (stored as JSON).
        last_reaction_at (datetime | None): Timestamp of the user's most recent reaction.
        created_at (datetime): When the user record was first created in our DB.
        updated_at (datetime): When the user record was last updated.
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    role: Mapped[constants.Role] = mapped_column(
        Enum(constants.Role, name="user_role"),
        nullable=False,
    )
    reactions: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )
    last_reaction_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    @classmethod
    def new(
        cls,
        username: str,
        reactions: list,
        role: constants.Role = constants.Role.EXTERNAL,
        last_reaction_at: datetime | None = None,
    ) -> "User":
        """
        Creates a new User instance ready to be added to the database.
        Args:
            username (str): Username of the user (e.g., "valentinc94").
            role (constants.Role, optional): User classification. Defaults to EXTERNAL.
            reactions (list): Initial reaction counts (as list of dicts or structured data).
                Defaults to empty list.
            last_reaction_at (datetime | None, optional): Timestamp of their most recent reaction.
                Can be set later if not known yet.

        Returns:
            User: A new configured User instance.
        """

        return cls(
            username=username,
            role=role,
            reactions=reactions,
            last_reaction_at=last_reaction_at,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
