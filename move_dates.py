import os
import shutil
import re
from datetime import datetime

# Path to the root directory where the date-named folders are located
ROOT_DIR = '/Volumes/Photo backup'

# Path to the final directory where files should be moved
FINAL_DIR = '/Volumes/Photo backup/final'

def get_month_name(month_number):
    """Convert a month number to its full month name."""
    return datetime.strptime(month_number, "%m").strftime("%B")

def move_files_by_date(root_dir, final_dir):
    """Find folders with date names and move their files to /year/month structure in the final directory."""
    # Regex to match folders like '20160714-124524'
    date_folder_pattern = re.compile(r'^(\d{4})(\d{2})\d{2}-\d{6}$')

    for dirpath, dirnames, _ in os.walk(root_dir):
        for dirname in dirnames:
            match = date_folder_pattern.match(dirname)
            if match:
                year, month = match.groups()
                month_name = get_month_name(month)

                source_folder = os.path.join(dirpath, dirname)
                dest_folder = os.path.join(final_dir, year, month_name)

                # Create the destination folder if it doesn't exist
                os.makedirs(dest_folder, exist_ok=True)

                # Move all files from the source folder to the destination folder
                for filename in os.listdir(source_folder):
                    source_file = os.path.join(source_folder, filename)
                    if os.path.isfile(source_file):
                        dest_file = os.path.join(dest_folder, filename)
                        try:
                            shutil.move(source_file, dest_file)
                            print(f"Moved: {source_file} -> {dest_file}")
                        except Exception as e:
                            print(f"Error moving {source_file}: {e}")

                # Delete the source folder if it's empty
                if not os.listdir(source_folder):
                    try:
                        os.rmdir(source_folder)
                        print(f"Deleted empty folder: {source_folder}")
                    except Exception as e:
                        print(f"Error deleting folder {source_folder}: {e}")

def main():
    print("Moving files from date-named folders to /year/month structure in final directory...")
    move_files_by_date(ROOT_DIR, FINAL_DIR)
    print("\nOperation complete!")

if __name__ == "__main__":
    main()