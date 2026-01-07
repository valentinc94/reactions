"""
Custom exceptions for the Users module.
"""


class UsernameAlreadyExists(Exception):
    """
    Raised when attempting to create a user with an username that already exists.
    """

    def __init__(self, username: str):
        super().__init__(f"The username '{username}' is already in use.")
        self.username = username


class UserDoesNotExist(Exception):
    """
    Raised when a user with the specified details does not exist.
    """

    def __init__(self):
        super().__init__("A user with the specified details does not exist.")
