"""
Pydantic schemas for common data structures and form validation.

This module defines the Pydantic models that are used across multiple modules in the application.
These schemas provide shared data structures used for validation and serialization of common
entities, such as API responses, request data, and form configurations.

Included are models for form fields and their attributes, which ensure that dynamic form data
is correctly validated and adheres to expected formats. These models are essential for maintaining
data integrity and consistency when handling user inputs or generating forms dynamically.

By leveraging these schemas, the application guarantees that the data exchanged between components
is well-defined, validated, and easy to serialize.
"""

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """
    Model to structure detailed error information in API responses.

    Attributes:
        code_transaction (str): A unique identifier for the type of error.
        message (str): A human-readable description providing more context about the error.
        request_id (str): A unique identifier for tracking the specific request that caused the error.
    """

    code_transaction: str = Field(
        ...,
        description="A unique identifier for the type of error.",
    )
    message: str = Field(
        ...,
        description="A human-readable description providing more context about the error.",
    )
    request_id: str = Field(
        ...,
        description="A unique identifier for tracking the specific request that caused the error.",
    )


class ErrorResponse(BaseModel):
    """
    Model to structure error responses in the API.

    Attributes:
        code_transaction (str): A unique identifier for the overall error response.
        detail (ErrorDetail): A nested model containing detailed information about the error.
    """

    code_transaction: str = Field(
        ...,
        description="A unique transaction code associated with the error.",
    )
    detail: ErrorDetail = Field(
        ...,
        description="An object containing specific details about the error.",
    )
