import os
import shutil

# Path to the root directory where the cleanup should happen
ROOT_DIR = '/Volumes/Photo backup/misc_from_internet'


def delete_unwanted_files(root_dir):
    """Delete Thumbs.db and files starting with 'AlbumArt' in all folders and subfolders."""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if (filename.lower() == 'thumbs.db' or
                    filename.lower().startswith('facetile') or
                    filename.lower().endswith('.aae')):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


def delete_empty_folders(root_dir):
    """Recursively delete empty folders, including those in the root directory, skipping system-protected folders."""
    protected_folders = {'.Spotlight-V100', '.Trashes', '.fseventsd', '.TemporaryItems'}

    # Walk the directory tree in bottom-up order
    for dirpath, dirnames, _ in os.walk(root_dir, topdown=False):
        # Skip protected folders
        dirnames[:] = [d for d in dirnames if d not in protected_folders]

        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            try:
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)
                    print(f"Deleted empty folder: {folder_path}")
            except Exception as e:
                print(f"Error deleting folder {folder_path}: {e}")

    # Check and delete empty folders directly in the root directory
    for entry in os.listdir(root_dir):
        entry_path = os.path.join(root_dir, entry)
        if entry in protected_folders:
            continue
        try:
            if os.path.isdir(entry_path) and not os.listdir(entry_path):
                os.rmdir(entry_path)
                print(f"Deleted empty folder in root: {entry_path}")
        except PermissionError as e:
            print(f"Permission error accessing {entry_path}: {e}")
        except Exception as e:
            print(f"Error deleting root folder {entry_path}: {e}")


def main():
    print("Deleting Thumbs.db and AlbumArt files...")
    delete_unwanted_files(ROOT_DIR)

    print("\nDeleting empty folders...")
    delete_empty_folders(ROOT_DIR)

    print("\nCleanup complete!")


if __name__ == "__main__":
    main()