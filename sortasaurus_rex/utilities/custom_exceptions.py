"""
Custom exception classes
"""


class DirectoryError(Exception):
    """Custom exception raised for directory-related errors."""


class PermissionDeniedError(Exception):
    """
    Custom exception raised when permission is denied
    for a directory operation.
    """


class EmptyDirectoryError(Exception):
    """
    Custom exception raised when the source directory
    is empty.
    """
