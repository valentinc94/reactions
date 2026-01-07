"""
Constants and enums for users.

Defines enumerations for user-related attributes, such as department, role, and onboarding status.
"""

from enum import Enum


class Role(str, Enum):
    """
    Represents the roles users can have in the system.
    """

    ADMIN = "admin"
    INTERNAL = "internal"
    EXTERNAL = "external"
