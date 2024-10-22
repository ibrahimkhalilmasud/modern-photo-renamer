# Modern Photo Renamer

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

Modern Photo Renamer is a Python application with a graphical user interface (GUI) that allows users to rename multiple photos based on information from an Excel file. This tool is particularly useful for organizing large collections of photos, such as product images or event photographs.

## Features

- User-friendly GUI built with customtkinter
- Excel file integration for photo renaming data
- Multiple photo directory support
- Customizable output directory
- Dark mode toggle
- Progress bar for renaming process
- Real-time logging of the renaming process
- Last result summary

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installation

Follow these steps to set up the Modern Photo Renamer on your system:

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/yourusername/modern-photo-renamer.git
   cd modern-photo-renamer
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Modern Photo Renamer, follow these steps:

1. Ensure you're in the project directory and your virtual environment is activated (if you're using one).

2. Run the application:
   ```
   python gui_renamer.py
   ```

3. Using the application:
   a. Click the "Browse" button next to "Excel File" to select your Excel file containing the renaming data.
   b. Click the "Add" button next to "Photos Directories" to add one or more directories containing the photos you want to rename.
   c. Click the "Browse" button next to "Output Directory" to select where the renamed photos will be saved.
   d. Click the "Rename Photos" button to start the renaming process.
   e. The progress bar will show the progress of the renaming process.
   f. The log display will show real-time information about the renaming process.
   g. The "Last Result" at the bottom will show whether the last operation was successful or encountered an error.

4. You can toggle between light and dark mode using the "Dark Mode" switch.

## Excel File Format

The Excel file should have the following columns:
- DESIGN
- ARTICLE
- QUALITY
- QTY

The application will use this information to rename the photos according to the pattern:
`{counter}. {DESIGN}_{ARTICLE}_{QUALITY}_{QTY}.{original_extension}`

## Troubleshooting

If you encounter any issues:

1. Make sure all required packages are installed correctly.
2. Check that your Excel file is in the correct format.
3. Ensure you have read and write permissions for the input and output directories.
4. Check the log display in the application for any error messages.

If problems persist, please open an issue on the GitHub repository with a detailed description of the problem and any error messages you're seeing.

## Contributing

Contributions to the Modern Photo Renamer are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure your code adheres to the existing style and includes appropriate tests and documentation.

## License

This project is licensed under the MIT License. See the LICENSE file for details.