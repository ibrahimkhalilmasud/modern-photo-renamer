#!/usr/bin/env python

import os
import pandas as pd
from PIL import Image
import logging
from datetime import datetime
import json
import re

def setup_logging(log_queue):
    """
    Set up logging to both queue (for GUI) and file.
    Creates a log file with a timestamp in the filename.
    """
    log_filename = f"renaming_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    class QueueHandler(logging.Handler):
        def emit(self, record):
            log_queue.put(self.format(record))
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    queue_handler = QueueHandler()
    queue_handler.setFormatter(formatter)
    logger.addHandler(queue_handler)

def load_last_used_folders():
    """
    Load last used folders from JSON file.
    Returns an empty dictionary if the file doesn't exist.
    """
    try:
        with open('last_used_folders.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_last_used_folders(folders):
    """
    Save last used folders to JSON file.
    """
    with open('last_used_folders.json', 'w') as f:
        json.dump(folders, f)

def normalize_design_code(code):
    """
    Remove non-alphanumeric characters and convert to uppercase.
    This helps in matching design codes from filenames to Excel data.
    """
    return re.sub(r'[^A-Z0-9]', '', code.upper())

def rename_photos(excel_path, photos_dir, output_dir, log_queue, progress_callback=None):
    """
    Main function to rename photos based on Excel data.
    
    Args:
    excel_path (str): Path to the Excel file containing photo data.
    photos_dir (str): Directory containing the photos to be renamed.
    output_dir (str): Directory where renamed photos will be saved.
    log_queue (queue.Queue): Queue for logging messages to GUI.
    progress_callback (function): Callback function to update progress in GUI.
    """
    setup_logging(log_queue)
    
    # Read Excel file
    df = pd.read_excel(excel_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store Excel data
    # Key: Normalized DESIGN, Value: tuple of (DESIGN, ARTICLE, QUALITY, QTY)
    data_dict = {}
    for _, row in df.iterrows():
        key = normalize_design_code(row['DESIGN'])
        value = (row['DESIGN'], row['ARTICLE'], row['QUALITY'], row['QTY'])
        data_dict[key] = value
    
    total_files = len([f for f in os.listdir(photos_dir) if os.path.isfile(os.path.join(photos_dir, f))])
    processed_files = 0
    renamed_files = 0
    
    # Counter for new file numbering
    file_counter = 1
    
    # Rename photos
    for filename in os.listdir(photos_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            processed_files += 1
            file_path = os.path.join(photos_dir, filename)
            
            # Extract the design code from the filename
            match = re.search(r'([A-Za-z]{3,4}-?\d+\s?[A-Za-z]?)', filename)
            if match:
                design = normalize_design_code(match.group(1))
                
                # Try to find a match in the data dictionary
                matched_key = next((key for key in data_dict if key.startswith(design)), None)
                
                if matched_key:
                    # If we find a match in our Excel data
                    full_design, article, quality, qty = data_dict[matched_key]
                    
                    # Construct the new filename using the counter
                    new_name = f"{file_counter}. {full_design}_{article}_{quality}_{qty}.{filename.split('.')[-1]}"
                    new_path = os.path.join(output_dir, new_name)
                    
                    # Open the image and preserve its orientation
                    with Image.open(file_path) as img:
                        # Save the image without changing its orientation
                        img.save(new_path, exif=img.info.get('exif'))
                    
                    logging.info(f"Renamed and saved: {filename} -> {new_name}")
                    renamed_files += 1
                    file_counter += 1  # Increment the counter
                else:
                    # If we don't find a match, log a warning
                    logging.warning(f"No match found for: {filename}")
            else:
                # If we can't extract a design code, log a warning
                logging.warning(f"Unable to extract design code from: {filename}")
            
            if progress_callback:
                progress_callback((processed_files / total_files) * 100)
    
    logging.info(f"Total files processed: {total_files}")
    logging.info(f"Files renamed: {renamed_files}")
    logging.info("Renaming process completed.")

if __name__ == "__main__":
    # This block is for testing purposes and won't be executed when imported as a module
    excel_path = "path/to/your/excel/file.xlsx"
    photos_dir = "path/to/your/photos/directory"
    output_dir = "path/to/output/directory"
    rename_photos(excel_path, photos_dir, output_dir, None)