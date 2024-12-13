import os
import shutil
import xxhash
from collections import defaultdict
from tqdm import tqdm

# Folder paths
ROOT_DIR = '/Volumes/Photo backup/photos'
ORIGINALS_DIR = '/Volumes/Photo backup/photos/originals'
COPIES_DIR = '/Volumes/Photo backup/photos/copies'

# List of photo and video file extensions (case insensitive)
PHOTO_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.heic', '.webp',
    '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg', '.3gp', '.mts', '.m4v', '.mpg'
}

def is_photo(filename):
    """Check if a file is a photo based on its extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower() in PHOTO_EXTENSIONS

def calculate_hash(file_path):
    """Calculate xxHash of a file."""
    hash_xx = xxhash.xxh64()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_xx.update(chunk)
        return hash_xx.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

def find_all_photos_with_hashes(root_dir):
    """Walk through the root directory and find all photos, storing them by hash."""
    files_by_hash = defaultdict(list)
    file_list = []

    # Collect all eligible files first
    print("Collecting photo files...")
    for dirpath, _, filenames in tqdm(os.walk(root_dir), desc="Scanning directories", unit="dir"):
        for filename in filenames:
            if is_photo(filename):
                file_list.append(os.path.join(dirpath, filename))

    # Process each file with a progress bar
    print("\nHashing photo files...")
    for file_path in tqdm(file_list, desc="Hashing files", unit="file"):
        file_hash = calculate_hash(file_path)
        if file_hash:
            files_by_hash[file_hash].append(file_path)

    return files_by_hash

def move_duplicates_from_originals(files_by_hash, originals_dir, copies_dir):
    """Move duplicates in originals to copies if they exist elsewhere on the drive."""
    os.makedirs(copies_dir, exist_ok=True)  # Ensure copies directory exists

    originals_count = sum(1 for paths in files_by_hash.values() if any(p.startswith(originals_dir) for p in paths))
    print(f"\nChecking for duplicates in {originals_count} files in originals...")

    with tqdm(total=originals_count, desc="Moving duplicates", unit="file") as pbar:
        for file_hash, paths in files_by_hash.items():
            originals = [path for path in paths if path.startswith(originals_dir)]
            non_originals = [path for path in paths if not path.startswith(originals_dir)]

            # If a file in originals has a duplicate elsewhere, move the original to copies
            if originals and non_originals:
                for original_path in originals:
                    dest_path = os.path.join(copies_dir, os.path.basename(original_path))
                    try:
                        shutil.move(original_path, dest_path)
                        print(f"Moved duplicate: {original_path} -> {dest_path}")
                        pbar.update(1)
                    except Exception as e:
                        print(f"Error moving {original_path}: {e}")
            else:
                pbar.update(len(originals))

def main():
    print("Starting final duplicate check...\n")

    # Step 1: Find all photos and their hashes
    files_by_hash = find_all_photos_with_hashes(ROOT_DIR)

    # Step 2: Move duplicates from originals to copies
    move_duplicates_from_originals(files_by_hash, ORIGINALS_DIR, COPIES_DIR)

    print("\nOperation complete!")

if __name__ == "__main__":
    main()