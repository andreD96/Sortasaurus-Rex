#!/usr/bin/env python3

"""
File classification script
This script classifies files in a specified directory into
predefined categories based on their extensions.
"""
import logging
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from classifier import classify_files_in_directory

from custom_exceptions import PermissionDeniedError, DirectoryError, EmptyDirectoryError
from directories_handler import get_directory, create_category_directories

# Configure logging
logging.basicConfig(filename='file_classification.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main(directory=None):
    """
    Main function that coordinates the file classification process.

    Args:
        directory (str, optional): The path to the source directory. If not provided,
                                   prompts the user to enter the source directory path.
    """
    categories = {'.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images', '.bmp': 'Images',
                  '.heic': 'Images', '.txt': 'Text', '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
                  '.xls': 'Spreadsheets', '.xlsx': 'Spreadsheets', '.csv': 'Spreadsheets', '.mp3': 'Audio',
                  '.wav': 'Audio', '.ogg': 'Audio', '.mp4': 'Videos', '.mkv': 'Videos', '.mov': 'Videos',
                  'Others': 'Others'}

    if directory is None:
        directory = get_directory()

    directory_path = Path(directory)

    if not directory_path.is_dir():
        raise DirectoryError(
            f"Error: The directory '{directory}' does not exist or is not a directory."
        )

    create_category_directories(directory_path, set(categories.values()))

    total_files = sum(1 for _ in directory_path.rglob('*') if _.is_file())

    if total_files == 0:
        raise EmptyDirectoryError("The directory is empty. No files to classify.")

    with ThreadPoolExecutor() as executor:
        with tqdm(total=total_files, desc="Classifying files", unit="file") as pbar:
            classify_files_in_directory(directory_path, categories, pbar)

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
