#!/usr/bin/env python3

import os
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


# Function to classify a file
def classify_file(filename):
    # Find the file extension
    extension = filename.split('.')[-1].lower()

    # Flag to check if file has been moved
    moved = False

    # Iterate over the categories
    for category, extensions in categories.items():
        # If the extension matches one of the extensions in the category, move the file
        if extension in extensions:
            # Construct the file paths
            source_path = os.path.join(directory, filename)
            dest_path = os.path.join(directory, category, filename)

            # Move the file
            os.rename(source_path, dest_path)
            print(f'Moved {filename} to {category}')
            moved = True
            break

    # If the file wasn't moved, move it to the 'Other' directory
    if not moved:
        source_path = os.path.join(directory, filename)
        dest_path = os.path.join(directory, 'Other', filename)
        os.rename(source_path, dest_path)
        print(f'Moved {filename} to Other')


# Get the list of files in the directory
files = os.listdir(directory)

# Use tqdm to create a progress bar
with tqdm(total=len(files), desc="Classifying files", unit="file") as pbar:
    # Classify each file
    for filename in files:
        if os.path.isfile(os.path.join(directory, filename)):
            classify_file(filename)
        pbar.update(1)

print("File classification completed.")
