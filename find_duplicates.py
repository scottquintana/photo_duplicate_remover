import os
import shutil
import hashlib
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

def calculate_hash(file_path):
    """Calculate MD5 hash of a file."""
    try:
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        problem_files.append((file_path, str(e)))
        return None

def find_files_by_hash(root_dir):
    """Walk through the root directory and find photo and video files, storing them by hash."""
    files_by_hash = defaultdict(list)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:

            if is_photo_or_video(filename):
                file_path = os.path.join(dirpath, filename)
                file_hash = calculate_hash(file_path)
                print(f"Processing: {file_path}")
                if file_hash:
                    files_by_hash[file_hash].append(file_path)
    return files_by_hash

def move_file(src, dest):
    """Move a file and handle exceptions."""
    try:
        shutil.move(src, dest)
        print(f"Moved: {src} -> {dest}")
    except Exception as e:
        print(f"Error moving {src}: {e}")
        problem_files.append((src, str(e)))

def move_files(files_dict):
    """Move duplicates to /copies and originals to /originals."""
    for file_hash, paths in files_dict.items():
        if len(paths) > 1:
            # Move the first file to /originals, rest to /copies
            original = paths.pop(0)
            dest_original = os.path.join(ORIGINALS_DIR, os.path.basename(original))
            move_file(original, dest_original)

            for duplicate in paths:
                dest_copy = os.path.join(COPIES_DIR, os.path.basename(duplicate))
                move_file(duplicate, dest_copy)
        else:
            # Only one file found, move it to /originals
            original = paths[0]
            dest_original = os.path.join(ORIGINALS_DIR, os.path.basename(original))
            move_file(original, dest_original)

def main():
    create_dirs()
    print("Scanning for photo and video files...")
    files_dict = find_files_by_hash(ROOT_DIR)
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