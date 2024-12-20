import os
import shutil
import xxhash
from collections import defaultdict
from tqdm import tqdm
import re

# Folder paths
ROOT_DIR = '/Volumes/Photo backup'              # Existing drive
NEW_DRIVE_DIR = '/Volumes/Madison Backup/Photo Project 2020'      # New hard drive with potential new photos
FINAL_DIR = '/Volumes/Photo backup/final'       # Destination for unique files

# List of photo and video file extensions (case insensitive)
PHOTO_VIDEO_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.heic', '.webp',
    '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg', '.3gp', '.mts', '.m4v', '.mpg',
    '.doc', '.docx', '.xls', '.xlsx', '.pdf', '.ppt', '.pptx', '.txt', '.csv', '.zip', '.rar', '.7z'
}

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

    # Count the number of directories first for the progress bar
    dir_count = sum(1 for _ in os.walk(root_dir))

    # Initialize the progress bar for scanning directories
    with tqdm(total=dir_count, desc="Scanning Directories", unit="dir") as pbar:
        for dirpath, _, filenames in os.walk(root_dir):
            # Skip any directory that contains the word "thumbnail"
            if "thumbnail" in dirpath.lower():
                pbar.update(1)
                continue

            for filename in filenames:
                if is_photo_or_video(filename):
                    file_path = os.path.join(dirpath, filename)
                    file_list.append(file_path)

            pbar.update(1)  # Update the progress bar for each scanned directory

    # Process each file with a progress bar
    for file_path in tqdm(file_list, desc=f"Hashing Files in {root_dir}", unit="file"):
        file_hash = calculate_hash(file_path)
        if file_hash:
            files_by_hash[file_hash].append(file_path)

    return files_by_hash

def check_drive_accessibility(drive_dir):
    """Check if the drive is accessible."""
    if not os.path.exists(drive_dir):
        print(f"Error: Cannot access {drive_dir}. Please make sure the drive is connected.")
        return False

    print("Drive is connected")
    return True

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

def move_unique_files(existing_files_dict, new_files_dict):
    """Move unique files from the new drive to the final directory, maintaining folder preferences."""
    total_files = sum(len(paths) for paths in new_files_dict.values())
    with tqdm(total=total_files, desc="Moving Unique Files", unit="file") as pbar:
        for file_hash, paths in new_files_dict.items():
            if file_hash not in existing_files_dict:
                # Get the preferred folder name for the unique file
                unique_file, preferred_folder = get_preferred_folder(paths)
                move_file(unique_file, preferred_folder)
            pbar.update(len(paths))


def main():
    create_dirs()

    if not check_drive_accessibility(NEW_DRIVE_DIR):
        return

    print("Scanning existing drive for photo and video files...")
    existing_files_dict = find_files_by_hash(ROOT_DIR)

    # Check if the new drive is accessible before scanning
    if not check_drive_accessibility(NEW_DRIVE_DIR):
        return

    print("\nScanning new drive for photo and video files...")
    new_files_dict = find_files_by_hash(NEW_DRIVE_DIR)

    print("\nIdentifying and moving unique files to the final directory...")
    move_unique_files(existing_files_dict, new_files_dict)

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