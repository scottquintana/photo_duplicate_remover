import os
import shutil
import re

# Root directory containing the numbered folders
ROOT_DIR = '/Volumes/Photo backup'
DEST_DIR = '/Volumes/Photo backup/misc_from_internet'

# Regular expression to match folder names like 1.5, 2.1.2, 3.4, etc.
PATTERN = re.compile(r'^\d+(\.\d+)*$')


def move_files_to_misc(root_dir, dest_dir):
    """Move all files from specific subfolders (matching the pattern) into the destination folder."""
    os.makedirs(dest_dir, exist_ok=True)  # Create the destination directory if it doesn't exist

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        folder_name = os.path.basename(dirpath)

        # Only process folders that match the pattern
        if PATTERN.match(folder_name):
            for filename in filenames:
                src_path = os.path.join(dirpath, filename)
                dest_path = os.path.join(dest_dir, filename)
                try:
                    shutil.move(src_path, dest_path)
                    print(f"Moved: {src_path} -> {dest_path}")
                except Exception as e:
                    print(f"Error moving {src_path}: {e}")

            # Delete the folder if it's empty after moving the files
            if not os.listdir(dirpath):
                try:
                    os.rmdir(dirpath)
                    print(f"Deleted empty folder: {dirpath}")
                except Exception as e:
                    print(f"Error deleting folder {dirpath}: {e}")


def main():
    print(f"Moving files from numbered subfolders in '{ROOT_DIR}' to '{DEST_DIR}'...")
    move_files_to_misc(ROOT_DIR, DEST_DIR)
    print("\nOperation complete!")


if __name__ == "__main__":
    main()