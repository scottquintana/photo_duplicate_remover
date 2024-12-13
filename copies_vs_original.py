import os
import shutil
import xxhash
from collections import defaultdict
from tqdm import tqdm

# Folder paths
COPIES_DIR = '/Volumes/Photo backup/photos/copies'
ORIGINALS_DIR = '/Volumes/Photo backup/photos/originals'

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
            while chunk := f.read(8192):
                hash_xx.update(chunk)
        return hash_xx.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None


def get_hashes_from_folder(folder):
    """Calculate hashes for all photos in the folder with a progress bar."""
    hashes = set()
    file_list = []

    # Collect all photo files first
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            if is_photo(filename):
                file_list.append(os.path.join(dirpath, filename))

    # Process each file with a progress bar
    for file_path in tqdm(file_list, desc=f"Hashing files in {folder}", unit="file"):
        file_hash = calculate_hash(file_path)
        if file_hash:
            hashes.add(file_hash)

    return hashes


def move_unique_photos(copies_dir, originals_dir):
    """Move photos from copies to originals if they don't already exist in originals."""
    print("Calculating hashes for originals...")
    originals_hashes = get_hashes_from_folder(originals_dir)
    print(f"Found {len(originals_hashes)} unique photos in originals.\n")

    print("Processing photos in copies...")
    file_list = []

    # Collect all photo files in copies
    for dirpath, _, filenames in os.walk(copies_dir):
        for filename in filenames:
            if is_photo(filename):
                file_list.append(os.path.join(dirpath, filename))

    # Process each file with a progress bar
    for file_path in tqdm(file_list, desc="Comparing and moving files", unit="file"):
        file_hash = calculate_hash(file_path)

        if file_hash and file_hash not in originals_hashes:
            # Move the file to originals
            dest_path = os.path.join(originals_dir, os.path.basename(file_path))
            try:
                shutil.move(file_path, dest_path)
                print(f"Moved: {file_path} -> {dest_path}")
                # Add the new hash to the set
                originals_hashes.add(file_hash)
            except Exception as e:
                print(f"Error moving {file_path}: {e}")
        else:
            print(f"Duplicate found, keeping in copies: {file_path}")


def main():
    print("Starting comparison between copies and originals...\n")
    move_unique_photos(COPIES_DIR, ORIGINALS_DIR)
    print("\nOperation complete!")


if __name__ == "__main__":
    main()