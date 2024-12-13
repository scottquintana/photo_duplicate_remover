import os
import shutil

# Base path where the documents are stored
DOCUMENTS_DIR = '/Volumes/Photo backup/documents'

def flatten_redundant_subfolders(base_dir):
    """Flatten redundant subfolders where a folder contains a subfolder with the same name."""
    for dirpath, dirnames, _ in os.walk(base_dir):
        for dirname in dirnames:
            nested_folder = os.path.join(dirpath, dirname)
            parent_folder = os.path.basename(dirpath)

            # Check if the nested folder name matches the parent folder name
            if dirname == parent_folder:
                try:
                    # Move all contents from the nested folder to the parent folder
                    for item in os.listdir(nested_folder):
                        src = os.path.join(nested_folder, item)
                        dest = os.path.join(dirpath, item)
                        shutil.move(src, dest)
                        print(f"Moved: {src} -> {dest}")

                    # Remove the now-empty nested folder
                    os.rmdir(nested_folder)
                    print(f"Deleted empty folder: {nested_folder}")

                except Exception as e:
                    print(f"Error processing {nested_folder}: {e}")

def main():
    print(f"Flattening redundant subfolders in: {DOCUMENTS_DIR}")
    flatten_redundant_subfolders(DOCUMENTS_DIR)
    print("\nOperation complete!")

if __name__ == "__main__":
    main()