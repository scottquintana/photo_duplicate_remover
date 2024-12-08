import os
import shutil
from collections import defaultdict

# Folder paths
ROOT_DIR = '/Volumes/Photo backup'
COPIES_DIR = '/Volumes/Photo backup/copies'
ORIGINALS_DIR = '/Volumes/Photo backup/originals'

# List of photo and video file extensions (case insensitive)
PHOTO_VIDEO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.webp',
                          '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg', '.3gp', '.mts'}

# List to store problem files
problem_files = []

def create_dirs():
    """Create copies and originals directories if they don't exist."""
    os.makedirs(COPIES_DIR, exist_ok=True)
    os.makedirs(ORIGINALS_DIR, exist_ok=True)

def is_photo_or_video(filename):
    """Check if a file is a photo or video based on its extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower() in PHOTO_VIDEO_EXTENSIONS

def find_files_by_name_and_size(root_dir):
    """Walk through the root directory and find photo and video files, storing them by name and size."""
    files_by_name_and_size = defaultdict(list)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if is_photo_or_video(filename):
                file_path = os.path.join(dirpath, filename)
                try:
                    file_size = os.path.getsize(file_path)
                    files_by_name_and_size[(filename, file_size)].append(file_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    return files_by_name_and_size

def move_file(src, base_dir, dest_dir):
    """Move a file while preserving the closest folder structure."""
    relative_path = os.path.relpath(src, ROOT_DIR)
    dest_path = os.path.join(dest_dir, relative_path)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        shutil.move(src, dest_path)
        print(f"Moved: {src} -> {dest_path}")
    except Exception as e:
        print(f"Error moving {src}: {e}")
        problem_files.append((src, str(e)))

def move_files(files_dict):
    """Move duplicates to /copies and originals to /originals."""
    for (filename, size), paths in files_dict.items():
        if len(paths) > 1:
            # Move the first file to /originals, rest to /copies
            original = paths.pop(0)
            move_file(original, ROOT_DIR, ORIGINALS_DIR)

            for duplicate in paths:
                move_file(duplicate, ROOT_DIR, COPIES_DIR)
        else:
            # Only one file found, move it to /originals
            original = paths[0]
            move_file(original, ROOT_DIR, ORIGINALS_DIR)

def main():
    create_dirs()
    print("Scanning for photo and video files...")
    files_dict = find_files_by_name_and_size(ROOT_DIR)
    print("Moving files...")
    move_files(files_dict)

    # Print problem files at the end
    if problem_files:
        print("\nThe following files could not be moved due to permission errors or other issues:")
        for file_path, error in problem_files:
            print(f"{file_path} - {error}")
    else:
        print("\nAll files were moved successfully!")

    print("Done!")

if __name__ == "__main__":
    main()
