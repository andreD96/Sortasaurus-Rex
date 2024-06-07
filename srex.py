#!/usr/bin/env python3

import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from pathlib import Path

# Prompt the user for the source directory
directory = input("Please enter the source directory to be monitored: ")

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
    print(f"The directory {directory} does not exist.")
    exit(1)

# Create directories for each category
for category in categories.keys():
    category_path = directory_path / category
    category_path.mkdir(parents=True, exist_ok=True)


def classify_file(file_path):
    """
    Classify and move a file to the appropriate directory based on its extension.

    Parameters:
    file_path (Path): The path of the file to classify.

    Returns:
    tuple: The filename and the category it was moved to.
    """
    try:
        # Find the file extension
        extension = file_path.suffix.lower().lstrip('.')

        # Default to 'Other' category
        dest_category = 'Other'

        # Iterate over the categories
        for category, extensions in categories.items():
            # If the extension matches one of the extensions in the category, set the destination category
            if extension in extensions:
                dest_category = category
                break

        # Construct the destination path
        dest_path = directory_path / dest_category / file_path.name

        # Move the file
        file_path.rename(dest_path)
        return file_path.name, dest_category

    except FileNotFoundError:
        return file_path.name, 'FileNotFoundError'
    except PermissionError:
        return file_path.name, 'PermissionError'
    except Exception as e:
        return file_path.name, f'Error: {str(e)}'


# Get the list of files in the directory
files = [f for f in directory_path.iterdir() if f.is_file()]

# Check if there are no files to classify
if not files:
    print("The directory is empty. No files to classify.")
    exit(0)

# Use ThreadPoolExecutor to classify files in parallel
with ThreadPoolExecutor() as executor:
    # Use tqdm to create a progress bar
    with tqdm(total=len(files), desc="Classifying files", unit="file") as pbar:
        # Submit tasks to the executor
        futures = [executor.submit(classify_file, file_path) for file_path in files]

        # Process results as they complete
        for future in futures:
            filename, category = future.result()
            if category == 'FileNotFoundError':
                print(f'Error: {filename} not found')
            elif category == 'PermissionError':
                print(f'Error: Permission denied for {filename}')
            elif category.startswith('Error:'):
                print(f'{category} for file {filename}')
            else:
                print(f'Moved {filename} to {category}')
            pbar.update(1)

print("File classification completed.")
