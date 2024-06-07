#!/usr/bin/env python3

import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

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

# Create directories for each category
for category in categories.keys():
    os.makedirs(os.path.join(directory, category), exist_ok=True)


def classify_file(filename):
    """
    Classify and move a file to the appropriate directory based on its extension.

    Parameters:
    filename (str): The name of the file to classify.

    Returns:
    tuple: The filename and the category it was moved to.
    """
    try:
        # Find the file extension
        extension = filename.split('.')[-1].lower()

        # Default to 'Other' category
        dest_category = 'Other'

        # Iterate over the categories
        for category, extensions in categories.items():
            # If the extension matches one of the extensions in the category, set the destination category
            if extension in extensions:
                dest_category = category
                break

        # Construct the file paths
        source_path = os.path.join(directory, filename)
        dest_path = os.path.join(directory, dest_category, filename)

        # Move the file
        os.rename(source_path, dest_path)
        return filename, dest_category

    except FileNotFoundError:
        return filename, 'FileNotFoundError'
    except PermissionError:
        return filename, 'PermissionError'
    except Exception as e:
        return filename, f'Error: {str(e)}'


# Get the list of files in the directory
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Use ThreadPoolExecutor to classify files in parallel
with ThreadPoolExecutor() as executor:
    # Use tqdm to create a progress bar
    with tqdm(total=len(files), desc="Classifying files", unit="file") as pbar:
        # Submit tasks to the executor
        futures = [executor.submit(classify_file, filename) for filename in files]

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
