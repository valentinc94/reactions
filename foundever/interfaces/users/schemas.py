"""
Pydantic schema for user responses.

Includes the schema for user-related data structures.
"""

from typing import List

from pydantic import BaseModel, Field

from foundever.domains.users import schemas


class UserResponse(BaseModel):
    """
    Schema for the response of user creation or update.

    Attributes:
        code_transaction (str): A code indicating the result of the transaction (e.g., "OK" for success).
        user_id (str): The unique identifier of the user, either newly created or updated.
    """

    code_transaction: str = Field(
        ...,
        description="A code indicating the result of the transaction (e.g., 'OK' for success).",
    )
    user_id: str = Field(
        ...,
        description="The unique identifier of the user, either newly created or updated.",
    )


class DeleteResponse(BaseModel):
    """
    Schema for the response of a delete operation.

    Attributes:
        code_transaction (str): A code indicating the result of the delete operation
            (e.g., "OK" for success).
        message (str): A human-readable message describing the result of the operation.
    """

    code_transaction: str = Field(
        ...,
        description="A code indicating the result of the delete operation (e.g., 'OK' for success).",
    )
    message: str = Field(
        ...,
        description="Human-readable message confirming the delete operation.",
    )


class UserRetrieveResponse(BaseModel):
    """
    Schema for the response returned when retrieving users.

    Attributes:
        code_transaction (str): A string representing the status of the operation
            (e.g., "OK" for success, "ERROR" for failure).
        data (List[schemas.UserRetrieve]): The list of retrieved users.
    """

    code_transaction: str = Field(
        "OK",
        description="A string representing the status of the operation (e.g., 'OK' for success or 'ERROR' for failure).",
    )
    data: List[schemas.UserRetrieve] = Field(
        ...,
        description="The list of retrieved users.",
    )
