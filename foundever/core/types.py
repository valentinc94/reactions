"""
Type definitions for generic models.

This module defines reusable type variables to ensure type safety and flexibility across
different parts of the application. These type variables are designed to handle model
instances and schemas, providing consistency when working with SQLAlchemy models,
Pydantic schemas, or other similar constructs.

Type Variables:
    - Instance: Represents a generic placeholder for model instances, typically used for
      SQLAlchemy models or objects that interact with the database layer.
    - Schema: Represents a generic placeholder for Pydantic models, ensuring type safety
      when working with schemas derived from `BaseModel`.
"""

from typing import TypeVar

from pydantic import BaseModel

Instance = TypeVar("Instance")
Schema = TypeVar("Schema", bound=BaseModel)
