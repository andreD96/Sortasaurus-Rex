from custom_exceptions import PermissionDeniedError, DirectoryError


def get_directory():
    """
    Prompts the user to enter the source directory path.

    Returns:
        str: The path to the source directory entered by the user.
    """
    return input("Please enter the source directory to be monitored: ")


def create_category_directories(directory_path, categories):
    """
    Creates subdirectories for each category within the specified directory.

    Args:
        directory_path (Path): The path to the directory where subdirectories
                               will be created.
        categories (list): A list of category names to be used
                           as subdirectory names.

    Raises:
        PermissionDeniedError: If permission is denied to create a directory.
        DirectoryError: For other directory-related errors during creation.
    """
    for category in categories:
        category_path = directory_path / category
        try:
            category_path.mkdir(parents=True, exist_ok=True)
        except PermissionError as exc:
            raise PermissionDeniedError(
                f"Error: Permission denied to create directory '{category_path}'."
            ) from exc
        except Exception as e:
            raise DirectoryError(f"Error: {e}") from e