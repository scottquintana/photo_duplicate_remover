import os
import shutil
import re

# Paths
ROOT_DIR = '/Volumes/Photo backup/final'  # Directory where your final folders are
THUMBNAILS_DIR = '/Volumes/Photo backup/final/thumbnails'  # Directory to move thumbnails

# Regular expression to match folders with exactly 21 characters, no spaces or underscores
THUMBNAIL_FOLDER_PATTERN = re.compile(r'^(?=.{22}$)[^\s_]*$')


def create_thumbnails_dir():
    """Create the thumbnails directory if it doesn't exist."""
    os.makedirs(THUMBNAILS_DIR, exist_ok=True)


def is_thumbnail_folder(folder_name):
    """Check if a folder name matches the thumbnail folder pattern (exactly 21 characters, no spaces or underscores)."""
    match = bool(THUMBNAIL_FOLDER_PATTERN.match(folder_name))
    print(f"Checking folder: '{folder_name}' - {'MATCH' if match else 'NO MATCH'}")
    return match


def move_files_from_thumbnail_folders(root_dir, thumbnails_dir):
    """Find thumbnail folders, move their files, and delete the folders."""
    for dirpath, dirnames, _ in os.walk(root_dir):
        for folder in dirnames:
            folder_path = os.path.join(dirpath, folder)
            if is_thumbnail_folder(folder):
                print(f"Processing thumbnail folder: {folder_path}")

                # Move all files from the thumbnail folder to the thumbnails directory
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        dest_path = os.path.join(thumbnails_dir, filename)
                        os.makedirs(thumbnails_dir, exist_ok=True)
                        try:
                            shutil.move(file_path, dest_path)
                            print(f"Moved: {file_path} -> {dest_path}")
                        except Exception as e:
                            print(f"Error moving {file_path}: {e}")

                # Check if the folder is empty and delete it
                if not os.listdir(folder_path):
                    try:
                        os.rmdir(folder_path)
                        print(f"Deleted empty folder: {folder_path}")
                    except Exception as e:
                        print(f"Error deleting {folder_path}: {e}")


def main():
    create_thumbnails_dir()
    move_files_from_thumbnail_folders(ROOT_DIR, THUMBNAILS_DIR)
    print("Thumbnail processing complete!")

if __name__ == "__main__":
    main()
