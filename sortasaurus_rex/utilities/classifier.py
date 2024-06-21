"""
Classifying functions
"""
import logging
from pathlib import Path
from typing import Dict, Tuple
from tqdm import tqdm

from .custom_exceptions import PermissionDeniedError, DirectoryError

# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


def classify_file(
        file_path: Path,
        root_directory_path: Path,
        categories: Dict[str, str]) -> Tuple[str, str]:
    """
    Classifies a file based on its extension and moves it
    to the appropriate category directory.

    Args:
        file_path (Path): The path to the file to be classified.
        root_directory_path (Path): The root directory path where categories are located.
        categories (Dict[str, str]): A dictionary mapping file extensions to category names.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionDeniedError: If permission is denied to move the file.
        DirectoryError: For other directory-related errors during creation.

    Returns:
        Tuple[str, str]: The file name and the category it was moved to.
    """
    if not file_path.exists():
        raise FileNotFoundError("File not found: %s" % file_path)

    file_ext = file_path.suffix.lower()
    category = categories.get(file_ext, "Others")
    dest_dir = root_directory_path / category

    # Check if the file is already in the correct category directory
    if file_path.parent == dest_dir:
        logging.info(
            "File %s is already in the correct category directory. Skipping move.",
            file_path.name
        )
        return file_path.name, category

    dest_path = dest_dir / file_path.name

    if dest_path.exists():
        logging.info("File %s already exists in %s. Skipping move.", file_path.name, category)
        return file_path.name, category

    try:
        file_path.rename(dest_path)
        logging.info("Moved %s to %s.", file_path.name, category)
        return file_path.name, category
    except PermissionError as exc:
        logging.error(
            "Permission denied to move file '%s' to '%s'.", file_path, dest_path,
            exc_info=True
        )
        raise PermissionDeniedError(
            "Error: Permission denied to move file '%s' to '%s'." % (file_path, dest_path)
        ) from exc
    except Exception as e:
        logging.error(
            "Error moving file '%s' to '%s': %s", file_path, dest_path, e,
            exc_info=True
        )
        raise DirectoryError("Error: %s" % e) from e


def classify_files_in_directory(
        directory_path: Path,
        categories: Dict[str, str],
        pbar: tqdm) -> None:
    """
    Classifies files in the given directory, including nested
    directories, and updates the progress bar.

    Args:
        directory_path (Path): The path to the directory to be classified.
        categories (Dict[str, str]): A dictionary mapping file extensions to category names.
        pbar (tqdm): The progress bar to update.
    """
    for file_path in directory_path.iterdir():
        if file_path.is_file():
            try:
                classify_file(file_path, directory_path, categories)
            except (FileNotFoundError, PermissionDeniedError, DirectoryError) as e:
                logging.error("%s", e, exc_info=True)
            pbar.update(1)
        elif file_path.is_dir():
            classify_files_in_directory(file_path, categories, pbar)
