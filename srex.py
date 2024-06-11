#!/usr/bin/env python3

"""
File classification script
This script classifies files in a specified directory into
predefined categories based on their extensions.
"""

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


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
        except PermissionError as exc:  # More specific exception handling
            raise PermissionDeniedError(
                f"Error: Permission denied to create directory '{category_path}'."
            ) from exc  # Chain the exceptions
        except Exception as e:
            raise DirectoryError(f"Error: {e}") from e


def classify_file(file_path, directory_path, categories):
    """
    Classify and move a file to the appropriate directory based on its extension.

    Parameters:
    file_path (Path): The path of the file to classify.
    directory_path (Path): The path of the source directory.
    categories (dict): Dictionary of categories and their extensions.

    Returns:
    tuple: The filename and the category it was moved to, or raises an exception on error.
    """
    try:
        # Find the file extension
        extension = file_path.suffix.lower().lstrip('.')

        # Default to 'Other' category
        dest_category = 'Other'

        # Iterate over the categories
        for the_category, each_extensions in categories.items():
            # If the extension matches one of the extensions
            # in the category, set the destination category
            if extension in each_extensions:
                dest_category = the_category
                break

        # Construct the destination path
        dest_path = directory_path / dest_category / file_path.name

        # Move the file
        file_path.rename(dest_path)
        return file_path.name, dest_category

    except FileNotFoundError as exc:  # More specific exception type
        raise FileNotFoundError(f"Error: {file_path} not found.") from exc
    except PermissionError as exc:  # More specific exception type
        raise PermissionDeniedError(f"Error: Permission denied for {file_path}.") from exc
    except Exception as e:
        raise DirectoryError(f"Error: {str(e)}") from e


def main():
    """Main function to run the file classification script."""
    # Prompt the user for the source directory
    directory = get_directory()

    # Dictionary of file categories and their extensions
    categories = {
        'Images': ['jpeg', 'jpg', 'png'],
        'PDFs': ['pdf'],
        'Datasets': ['csv', 'xlsx', 'json'],
        'Videos&ShortVids': ['mp4', 'gif'],
        'Other': []  # Directory for files that don't match any category
    }

    # Convert the directory to a Path object
    directory_path = Path(directory)

    # Check if the directory exists
    if not directory_path.is_dir():
        raise DirectoryError(
            f"Error: The directory '{directory}' does not exist or is not a directory."
        )

    # Create directories for each category
    create_category_directories(directory_path, categories)

    # Get the list of files in the directory
    try:
        files = [f for f in directory_path.iterdir() if f.is_file()]
    except PermissionError as exc:  # More specific exception type
        raise PermissionDeniedError(
            f"Error: Permission denied to access directory '{directory_path}'."
        ) from exc
    except Exception as e:
        raise DirectoryError(f"Error: {e}") from e

    # Check if there are no files to classify
    if not files:
        raise EmptyDirectoryError("The directory is empty. No files to classify.")

    # Use ThreadPoolExecutor to classify files in parallel
    with ThreadPoolExecutor() as executor:
        # Use tqdm to create a progress bar
        with tqdm(total=len(files), desc="Classifying files", unit="file") as pbar:
            # Submit tasks to the executor
            futures = [executor.submit(
                classify_file, file_path, directory_path, categories
            ) for file_path in files]

            # Process results as they complete
            for future in futures:
                try:
                    filename, category = future.result()
                    print(f"Moved {filename} to {category}.")
                except FileNotFoundError as e:
                    print(e)
                except PermissionDeniedError as e:
                    print(e)
                except DirectoryError as e:
                    print(e)
                pbar.update(1)

    print("File classification completed.")


if __name__ == '__main__':
    try:
        main()
    except DirectoryError as e:
        print(e)
        sys.exit(1)
    except PermissionDeniedError as e:
        print(e)
        sys.exit(1)
    except EmptyDirectoryError as e:
        print(e)
        sys.exit(0)
