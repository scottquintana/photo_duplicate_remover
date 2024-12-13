import os
import shutil
import re

# Base directory containing the photo folders
PHOTOS_DIR = '/Volumes/Photo backup/photos'

# Valid year range
VALID_YEAR_RANGE = range(1990, 2025)


def format_folder_name(name):
    """Format the folder name by converting it to lowercase and removing extra spaces."""
    return name.strip().lower()


def move_folders_by_year(base_dir):
    """Move folders with month/event year names to better-formatted year subfolders."""
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        # Skip if it's not a directory
        if not os.path.isdir(folder_path):
            continue

        # Regex to match names like 'December 2012', 'christmas 2007', 'feb 2003'
        match = re.match(r'^(.+?)\s*(\d{4})$', folder_name, re.IGNORECASE)

        if match:
            event_name, year_str = match.groups()
            year = int(year_str)

            # Check if the year is within the valid range
            if year in VALID_YEAR_RANGE:
                # Format the event name (e.g., 'December' -> 'december')
                formatted_event_name = format_folder_name(event_name)

                # Construct the destination path
                dest_dir = os.path.join(base_dir, str(year), formatted_event_name)

                # Create the destination directory if it doesn't exist
                os.makedirs(dest_dir, exist_ok=True)

                # Move the folder to the new location
                dest_path = os.path.join(dest_dir, os.path.basename(folder_path))
                try:
                    shutil.move(folder_path, dest_path)
                    print(f"Moved: {folder_path} -> {dest_path}")
                except Exception as e:
                    print(f"Error moving {folder_path}: {e}")


def main():
    print(f"Reorganizing folders in '{PHOTOS_DIR}'...")
    move_folders_by_year(PHOTOS_DIR)
    print("\nOperation complete!")


if __name__ == "__main__":
    main()