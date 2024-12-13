import os
import shutil

# Folder paths
FINAL_DIR = '/Volumes/Photo backup/misc_from_internet'
DOCUMENTS_DIR = '/Volumes/Photo backup/documents'

# List of document file extensions (case insensitive)
DOCUMENT_EXTENSIONS = {
    '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf',
    '.odt', '.ods', '.odp', '.csv', '.pages', '.numbers', '.key', '.zip'
}

def is_document(filename):
    """Check if a file is a document based on its extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower() in DOCUMENT_EXTENSIONS

def move_documents(final_dir, documents_dir):
    """Move individual document files to the documents directory, preserving folder structure."""
    for dirpath, _, filenames in os.walk(final_dir, topdown=False):
        for filename in filenames:
            if is_document(filename):
                # Get the relative path to preserve folder structure
                relative_path = os.path.relpath(dirpath, final_dir)
                destination_path = os.path.join(documents_dir, relative_path)

                # Create the destination directory if it doesn't exist
                os.makedirs(destination_path, exist_ok=True)

                # Move the document file
                src_path = os.path.join(dirpath, filename)
                dest_path = os.path.join(destination_path, filename)
                try:
                    shutil.move(src_path, dest_path)
                    print(f"Moved: {src_path} -> {dest_path}")
                except Exception as e:
                    print(f"Error moving {src_path}: {e}")

        # Delete the folder if it's empty after moving the documents
        if not os.listdir(dirpath):
            try:
                os.rmdir(dirpath)
                print(f"Deleted empty folder: {dirpath}")
            except Exception as e:
                print(f"Error deleting folder {dirpath}: {e}")

def main():
    print("Moving document files to the documents directory...")
    move_documents(FINAL_DIR, DOCUMENTS_DIR)
    print("\nOperation complete!")

if __name__ == "__main__":
    main()