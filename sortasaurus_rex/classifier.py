import logging
from pathlib import Path
from tqdm import tqdm

from custom_exceptions import PermissionDeniedError, DirectoryError


def classify_file(file_path, root_directory_path, categories):
    """
    Classifies a file based on its extension and moves it
    to the appropriate category directory.

    Args:
        file_path (Path): The path to the file to be classified.
        root_directory_path (Path): The root directory path where categories are located.
        categories (dict): A dictionary mapping file extensions to category names.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionDeniedError: If permission is denied to move the file.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_ext = file_path.suffix.lower()
    category = categories.get(file_ext, "Others")
    dest_dir = root_directory_path / category

    dest_path = dest_dir / file_path.name

    if dest_path.exists():
        logging.info(f"File {file_path.name} already exists in {category}. Skipping move.")
        return file_path.name, category

    try:
        file_path.rename(dest_path)
        logging.info(f"Moved {file_path.name} to {category}.")
        return file_path.name, category
    except PermissionError as exc:
        logging.error(f"Permission denied to move file '{file_path}' to '{dest_path}'.")
        raise PermissionDeniedError(
            f"Error: Permission denied to move file '{file_path}' to '{dest_path}'."
        ) from exc
    except Exception as e:
        logging.error(f"Error moving file '{file_path}' to '{dest_path}': {e}")
        # Check if the file is already in the correct category directory
        if file_path.parent == dest_dir:
            logging.info(f"File {file_path.name} is already in the correct category directory. Skipping move.")
            return file_path.name, category


def classify_files_in_directory(directory_path, categories, pbar):
    """
    Classifies files in the given directory, including nested
    directories, and updates the progress bar.

    Args:
        directory_path (Path): The path to the directory to be classified.
        categories (dict): A dictionary mapping file extensions to category names.
        pbar (tqdm): The progress bar to update.
    """
    for file_path in directory_path.iterdir():
        if file_path.is_file():
            try:
                classify_file(file_path, directory_path, categories)
            except (FileNotFoundError, PermissionDeniedError, DirectoryError) as e:
                print(e)
            pbar.update(1)
        elif file_path.is_dir():
            classify_files_in_directory(file_path, categories, pbar)
