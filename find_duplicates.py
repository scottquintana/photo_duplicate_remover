import os
import shutil
import xxhash
from collections import defaultdict
from tqdm import tqdm
import re

# Folder paths
# ROOT_DIR = '/Volumes/Photo backup'
# FINAL_DIR = '/Volumes/Photo backup/final'
#
ROOT_DIR = '/run/media/scottquintana/BackupDrive2'
FINAL_DIR = '/run/media/scottquintana/BackupDrive2/final'

# List of photo and video file extensions (case insensitive)
PHOTO_VIDEO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.webp',
                          '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg', '.3gp', '.mts'}

# List to store problem files
problem_files = []

def create_dirs():
    """Create final directory if it doesn't exist."""
    os.makedirs(FINAL_DIR, exist_ok=True)

def is_photo_or_video(filename):
    """Check if a file is a photo or video based on its extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower() in PHOTO_VIDEO_EXTENSIONS

def calculate_hash(file_path):
    """Calculate xxHash of a file."""
    try:
        hash_xx = xxhash.xxh64()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_xx.update(chunk)
        return hash_xx.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        problem_files.append((file_path, str(e)))
        return None

def find_files_by_hash(root_dir):
    """Walk through the root directory and find photo and video files, storing them by hash."""
    files_by_hash = defaultdict(list)
    file_list = []

    # Gather all eligible files first
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if is_photo_or_video(filename):
                file_path = os.path.join(dirpath, filename)
                file_list.append(file_path)

    # Process each file with a progress bar
    for file_path in tqdm(file_list, desc="Hashing Files", unit="file"):
        file_hash = calculate_hash(file_path)
        if file_hash:
            files_by_hash[file_hash].append(file_path)

    return files_by_hash

def get_preferred_folder(file_paths):
    """Return the preferred folder name, prioritizing named folders over year-only folders."""
    non_year_folders = []
    year_folders = []

    year_pattern = re.compile(r'^\d{4}$')

    for path in file_paths:
        closest_folder = os.path.basename(os.path.dirname(path))
        if year_pattern.match(closest_folder):
            year_folders.append((path, closest_folder))
        else:
            non_year_folders.append((path, closest_folder))

    # Prioritize non-year folders
    if non_year_folders:
        return non_year_folders[0]
    elif year_folders:
        return year_folders[0]
    else:
        # Fallback to the first path if no valid folder is found
        return file_paths[0], os.path.basename(os.path.dirname(file_paths[0]))

def move_file(src, folder_name):
    """Move a file to the final directory, using the specified folder name."""
    try:
        dest_dir = os.path.join(FINAL_DIR, folder_name)
        os.makedirs(dest_dir, exist_ok=True)

        dest_path = os.path.join(dest_dir, os.path.basename(src))

        shutil.move(src, dest_path)
        print(f"Moved: {src} -> {dest_path}")
    except Exception as e:
        print(f"Error moving {src}: {e}")
        problem_files.append((src, str(e)))

def move_unique_files(files_dict):
    """Move one unique copy of each file to the final directory."""
    total_files = sum(len(paths) for paths in files_dict.values())
    with tqdm(total=total_files, desc="Moving Files", unit="file") as pbar:
        for file_hash, paths in files_dict.items():
            # Get the preferred folder name for the unique file
            unique_file, preferred_folder = get_preferred_folder(paths)
            move_file(unique_file, preferred_folder)
            pbar.update(len(paths))

def main():
    create_dirs()
    print("Scanning for photo and video files...")
    files_dict = find_files_by_hash(ROOT_DIR)
    print("Moving files to the final directory...")
    move_unique_files(files_dict)

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
