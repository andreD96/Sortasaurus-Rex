
# Sortasaurus-Rex: File Classification Script

## Overview

This script classifies files in a specified directory into predefined categories based on their extensions. It uses multithreading to speed up the classification process and provides real-time progress updates using a progress bar. The script ensures that the source directory exists and is not empty before processing, and handles errors gracefully.

## Features

- **Automatic File Classification:** Automatically categorizes files based on their extensions.
- **Multithreading:** Utilizes `ThreadPoolExecutor` to classify files in parallel for faster processing.
- **Progress Bar:** Uses `tqdm` to display a real-time progress bar during the classification process.
- **Robust Path Handling:** Utilizes `pathlib` for handling file and directory paths.
- **Error Handling:** Provides detailed error messages and handles common file operation errors like `FileNotFoundError` and `PermissionError`.

## Prerequisites

- Python 3.6 or higher
- `tqdm` library

You can install `tqdm` using pip if it's not already installed:

```bash
pip install tqdm
```

## Usage

1. **Run the Script:**

   Execute the script from the command line:

   ```bash
   python srex.py
   ```

2. **Enter the Source Directory:**

   When prompted, enter the path to the directory you want to classify.

   ```plaintext
   Please enter the source directory to be monitored:
   ```

3. **Script Execution:**

   The script will classify the files into the following categories:
   - **Images:** `jpeg`, `jpg`, `png`
   - **PDFs:** `pdf`
   - **Datasets:** `csv`, `xlsx`, `json`
   - **Videos & ShortVids:** `mp4`, `gif`
   - **Other:** Files that do not match any of the above categories

   Each category will have its own directory created within the source directory.


4. **Completion:**

   The script will display the progress and log messages indicating where each file has been moved or if there were any errors.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [tqdm](https://github.com/tqdm/tqdm) for the progress bar implementation.
- Python community for various open-source contributions.
