import os
import shutil
import re

# Paths
ROOT_DIR = '/path/to/your/final'  # Set to the directory where your final folders are
THUMBNAILS_DIR = '/path/to/your/thumbnails'  # Set to where you want to move the thumbnails

# Regular expression to match 21-character folder names with no spaces
THUMBNAIL_FOLDER_PATTERN = re.compile(r'^[^\s]{21}$')


def create_thumbnails_dir():
    """Create the thumbnails directory if it doesn't exist."""
    os.makedirs(THUMBNAILS_DIR, exist_ok=True)


def is_thumbnail_folder(folder_name):
    """Check if a folder name matches the thumbnail folder pattern."""
    return bool(THUMBNAIL_FOLDER_PATTERN.match(folder_name))


def move_files_from_thumbnail_folders(root_dir, thumbnails_dir):
    """Find thumbnail folders, move their files, and delete the folders."""
    for dirpath, dirnames, _ in os.walk(root_dir):
        for folder in dirnames:
            if is_thumbnail_folder(folder):
                folder_path = os.path.join(dirpath, folder)
                print(f"Processing thumbnail folder: {folder_path}")

                # Move all files from the thumbnail folder to the thumbnails directory
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        dest_path = os.path.join(thumbnails_dir, filename)
                        shutil.move(file_path, dest_path)
                        print(f"Moved: {file_path} -> {dest_path}")

                # Check if the folder is empty and delete it
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)
                    print(f"Deleted empty folder: {folder_path}")


def main():
    create_thumbnails_dir()
    move_files_from_thumbnail_folders(ROOT_DIR, THUMBNAILS_DIR)
    print("Thumbnail processing complete!")


if __name__ == "__main__":
    main()
