"""
Pydantic schemas for the Users module.

This module defines Pydantic models used for data validation and serialization
in the Users domain. These schemas are used to define the structure and validation
rules for incoming and outgoing data related to user management, including user
creation, updates, authentication, and more.
"""

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from foundever.apps.users import constants


class Reactions(BaseModel):
    """
    Reactions counter.
    """

    plus_one: int = Field(
        default=0,
        ge=0,
        description="Number of 👍 reactions",
    )
    minus_one: int = Field(
        default=0,
        ge=0,
        description="Number of 👎 reactions",
    )
    laugh: int = Field(
        default=0,
        ge=0,
        description="Number of 😄 reactions",
    )
    confused: int = Field(
        default=0,
        ge=0,
        description="Number of 😕 reactions",
    )
    heart: int = Field(
        default=0,
        ge=0,
        description="Number of ❤️ reactions",
    )
    hooray: int = Field(
        default=0,
        ge=0,
        description="Number of 🎉 reactions",
    )
    rocket: int = Field(
        default=0,
        ge=0,
        description="Number of 🚀 reactions",
    )
    eyes: int = Field(
        default=0,
        ge=0,
        description="Number of 👀 reactions",
    )


class UserCreate(BaseModel):
    """
    Schema for ingesting or syncing a User into the database.
    """

    username: str = Field(
        ...,
        min_length=1,
        max_length=39,
        description="username (e.g., 'valentinc94')",
        examples=["bob_esponja", "calamardo"],
    )
    role: constants.Role = Field(
        default=constants.Role.EXTERNAL,
        description="User classification: EXTERNAL, INTERNAL, or ADMIN",
    )
    reactions: Reactions = Field(
        default_factory=Reactions,
        description="Aggregated reaction counts given by this user",
    )
    last_reaction_at: datetime | None = Field(
        None,
        description="Timestamp of the user's most recent reaction (UTC)",
    )


class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    """

    username: str = Field(
        ...,
        min_length=1,
        max_length=39,
        description="username (e.g., 'valentinc94')",
        examples=["bob_esponja", "calamardo"],
    )
    role: constants.Role | None = Field(
        default=constants.Role.EXTERNAL,
        description="User classification: EXTERNAL, INTERNAL, or ADMIN",
    )
    reactions: Reactions | None = Field(
        None,
        description="Aggregated reaction counts given by this user",
    )
    last_reaction_at: datetime | None = Field(
        None,
        description="Timestamp of the user's most recent reaction (UTC)",
    )

    @model_validator(mode="before")
    @classmethod
    def check_at_least_one_field(cls, values: dict) -> dict:
        """
        Ensures that at least one updatable field is provided.

        The fields considered for update are: role, reactions, last_reaction_at.

        Raises:
            ValueError: If no fields are provided for update.
        """
        updatable_fields = ["role", "reactions", "last_reaction_at"]
        provided = any(values.get(field) is not None for field in updatable_fields)

        if not provided:
            raise ValueError(
                "At least one field must be provided for update: "
                "role, reactions, or last_reaction_at"
            )
        return values


class UserRetrieve(BaseModel):
    """
    Schema for ingesting or syncing a User into the database.
    """

    id: str = Field(
        ...,
        description="Unique identifier of the user.",
    )
    username: str = Field(
        ...,
        description="Unique username of the user",
    )
    role: constants.Role = Field(
        description="User classification: EXTERNAL, INTERNAL, or ADMIN",
    )
    reactions: Reactions = Field(
        description="Aggregated reaction counts given by this user",
    )
    last_reaction_at: str | None = Field(
        None,
        description="Timestamp of the user's most recent reaction (UTC)",
    )
    created_at: str = Field(
        ...,
        description="The timestamp when the transaction was created.",
    )
    updated_at: str = Field(
        ...,
        description="The timestamp when the transaction was last updated.",
    )
