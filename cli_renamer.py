#!/usr/bin/env python

import argparse
from photo_renamer import rename_photos

def main():
    """
    Main function to handle command-line arguments and call the rename_photos function.
    """
    parser = argparse.ArgumentParser(description="Rename photos based on Excel data.")
    parser.add_argument("excel_path", help="Path to the Excel file")
    parser.add_argument("photos_dir", help="Path to the directory containing photos")
    parser.add_argument("output_dir", help="Path to the output directory for renamed photos")
    
    args = parser.parse_args()
    
    try:
        rename_photos(args.excel_path, args.photos_dir, args.output_dir)
        print("Photo renaming process completed. Check the log file for details.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()