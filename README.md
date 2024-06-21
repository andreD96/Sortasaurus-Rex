# Sortasaurus-Rex: File Classification Script

## Overview

This script classifies files in a specified directory into predefined categories based on their extensions. It uses multithreading to speed up the classification process and provides real-time progress updates using a progress bar. The script ensures that the source directory exists and is not empty before processing, and handles errors gracefully.

## Features
## Features

- **Intelligent File Classification:** Automatically categorizes files into Images, PDFs, Datasets, Videos & ShortVids, and Other.
- **High-Performance:** Utilizes multithreading via `ThreadPoolExecutor` for parallel processing.
- **Real-Time Progress:** Displays a live progress bar using `tqdm`.
- **Robust File Handling:** Uses `pathlib` for cross-platform compatibility.
- **Error Management:** Gracefully handles and logs common file operation errors.
- **Comprehensive Logging:** Records detailed process information and errors to both console and file.

## Prerequisites

- Python 3.6 or higher
- `tqdm` library

You can install `tqdm` using pip if it's not already installed:
```bash
pip install tqdm
```

## Installation

1. Ensure you have Python 3.6 or higher installed.
2. Install Sortasaurus-Rex using pip:

```bash
   pip install sortasaurus-rex
```

## Usage

1. **Run the Script:**

   Execute the script from the command line:

   ```bash
   srex
   ```

2. **Enter the Source Directory:**

   When prompted, enter the path to the directory you want to classify.

   ```plaintext
   Please enter the source directory to be monitored: /path/to/your/directory
   ```
   You can leave the value empty for the current working directory

3. **Script Execution:**

   Sortasaurus-Rex will process the files, displaying progress and creating the following category subdirectories:
   
   - **Images:** `jpeg`, `jpg`, `png`
   - **PDFs:** `pdf`
   - **Datasets:** `csv`, `xlsx`, `json`
   - **Videos & ShortVids:** `mp4`, `gif`
   - **Other:** Files that do not match any of the above categories

   Each category will have its own directory created within the source directory.

4. **Completion:**

   The script will display the progress and log messages indicating where each file has been moved or if there were any errors.

## Configuration

Currently, Sortasaurus-Rex uses predefined categories. Future versions may include customizable category definitions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [tqdm](https://github.com/tqdm/tqdm) for the progress bar implementation.
- Python community for various open-source contributions.

## Support
For issues, questions, or contributions, please open an issue on the GitHub repository.