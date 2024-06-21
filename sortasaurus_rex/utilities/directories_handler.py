"""
Directory handling functions
"""

import logging
from pathlib import Path
from typing import List
from .custom_exceptions import PermissionDeniedError, DirectoryError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_directory() -> str:
    """
    Prompts the user to enter the source directory path.

    Returns:
        str: The path to the source directory entered by the user.
    """
    return input("Please enter the source directory to be monitored: ")


def create_category_directories(directory_path: Path, categories: List[str]) -> None:
    """
    Creates subdirectories for each category within the specified directory.

    Args:
        directory_path (Path): The path to the directory where subdirectories
                               will be created.
        categories (List[str]): A list of category names to be used
                                as subdirectory names.

    Raises:
        PermissionDeniedError: If permission is denied to create a directory.
        DirectoryError: For other directory-related errors during creation.
    """
    for category in categories:
        category_path = directory_path / category
        try:
            category_path.mkdir(parents=True, exist_ok=True)
            logging.info(
                "Created directory '%s'.",
                category_path
            )
        except PermissionError as exc:
            logging.error(
                "Permission denied to create directory '%s'.",
                category_path,
                exc_info=True)
            raise PermissionDeniedError(
                "Error: Permission denied to create directory '%s'." % category_path
            ) from exc
        except Exception as e:
            logging.error("Error creating directory '%s': %s",
                          category_path, e,
                          exc_info=True
                          )
            raise DirectoryError("Error: %s" % e) from e
