# FileSorterIntoDirectories
 
This script classifies and moves files from a user-specified source directory into predetermined directories based on file extensions. The script uses multithreading to improve performance and includes a progress bar for visual feedback.

## How to Use

- Prompt for Source Directory: The script prompts the user to enter the source directory to be monitored.
- Create Category Directories: The script creates directories for each file category if they don't already exist.
- Classify Files: The script classifies files based on their extensions and moves them to the appropriate directory.
- Parallel Processing: Uses ThreadPoolExecutor to classify files in parallel.
- Progress Bar: Displays a progress bar using tqdm to show the classification progress.

### Error Handling
- FileNotFoundError: Handles cases where a file is not found (likely moved or deleted during processing).
- PermissionError: Handles permission errors that may occur during file operations.
- General Exception: Catches and reports any other exceptions that occur during file processing.

```shell
$ python3 do_sort.py
Please enter the source directory to be monitored: /path/to/source_directory
Classifying files: 100%|████████████████████████████████████████| 100/100 [00:05<00:00, 19.98file/s]
Moved file1.jpg to Images
Moved file2.pdf to PDFs
...
File classification completed.
```
