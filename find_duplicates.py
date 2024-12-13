import os
import shutil
import xxhash
from collections import defaultdict
from tqdm import tqdm
import re

# Folder paths
ROOT_DIR = '/Volumes/Photo backup/final'        # Existing sorted photos
TRANSFER_DIR = '/Volumes/Photo backup/transfer' # New photos to be sorted
FINAL_DIR = '/Volumes/Photo backup/final'       # Destination for unique files

# List of photo, video, and document file extensions (case insensitive)
PHOTO_VIDEO_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.heic', '.webp',
    '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg', '.3gp', '.mts', '.m4v', '.mpg',
    '.doc', '.docx', '.txt', '.zip'
}

# List to store problem files
problem_files = []

def create_dirs():
    """Create final directory if it doesn't exist."""
    os.makedirs(FINAL_DIR, exist_ok=True)

def is_photo_or_video(filename):
    """Check if a file is a photo, video, or document based on its extension."""
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
    """Walk through the root directory and find files, storing them by hash."""
    files_by_hash = defaultdict(list)
    file_list = []

    # Gather all eligible files first
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if is_photo_or_video(filename):
                file_path = os.path.join(dirpath, filename)
                file_list.append(file_path)

    # Process each file with a progress bar
    for file_path in tqdm(file_list, desc=f"Hashing Files in {root_dir}", unit="file"):
        file_hash = calculate_hash(file_path)
        if file_hash:
            files_by_hash[file_hash].append(file_path)

    return files_by_hash

def get_preferred_folder(file_path):
    """Return the closest folder name, prioritizing named folders over year-only folders."""
    year_pattern = re.compile(r'^\d{4}$')
    closest_folder = os.path.basename(os.path.dirname(file_path))
    return closest_folder if not year_pattern.match(closest_folder) else None

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

def move_unique_files(existing_files_dict, transfer_files_dict):
    """Move unique files from transfer directory to the final directory."""
    total_files = sum(len(paths) for paths in transfer_files_dict.values())
    with tqdm(total=total_files, desc="Moving Unique Files", unit="file") as pbar:
        for file_hash, paths in transfer_files_dict.items():
            if file_hash not in existing_files_dict:
                # Move the file using the preferred folder name
                for file_path in paths:
                    folder_name = get_preferred_folder(file_path) or "unsorted"
                    move_file(file_path, folder_name)
            pbar.update(len(paths))

def main():
    create_dirs()
    print("Scanning existing final directory for photo, video, and document files...")
    existing_files_dict = find_files_by_hash(ROOT_DIR)

    print("\nScanning transfer directory for photo, video, and document files...")
    transfer_files_dict = find_files_by_hash(TRANSFER_DIR)

    print("\nIdentifying and moving unique files to the final directory...")
    move_unique_files(existing_files_dict, transfer_files_dict)

    # Print problem files at the end
    if problem_files:
        print("\nThe following files could not be moved due to permission errors or other issues:")
        for file_path, error in problem_files:
            print(f"{file_path} - {error}")
    else:
        print("\nAll unique files were moved successfully!")

    print("Done!")

if __name__ == "__main__":
    main()