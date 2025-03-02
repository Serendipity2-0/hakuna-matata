import os
import csv
import shutil
import datetime
import platform
import mimetypes
import fnmatch
from pathlib import Path


def get_file_metadata(file_path):
    """Extract metadata from a file."""
    file_stat = os.stat(file_path)
    file_path = Path(file_path)

    # Get basic file information
    metadata = {
        "filename": file_path.name,
        "path": str(file_path),
        "size_bytes": file_stat.st_size,
        "size_mb": round(file_stat.st_size / (1024 * 1024), 2),
        "created_time": datetime.datetime.fromtimestamp(file_stat.st_ctime).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "modified_time": datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "accessed_time": datetime.datetime.fromtimestamp(file_stat.st_atime).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "extension": file_path.suffix.lower(),
        "mime_type": mimetypes.guess_type(str(file_path))[0] or "unknown",
        "source_folder": file_path.parent.name,
    }

    return metadata


def load_gitignore_patterns(directory):
    """Load patterns from .gitignore files in the given directory and its parents."""
    patterns = []
    current_dir = Path(directory)

    # Check current directory and all parent directories for .gitignore files
    while current_dir != current_dir.parent:  # Stop at root
        gitignore_path = current_dir / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith("#"):
                        patterns.append(line)
        current_dir = current_dir.parent

    return patterns


def should_ignore(file_path, ignore_patterns):
    """Check if a file should be ignored based on gitignore patterns."""
    file_path = Path(file_path)
    file_name = file_path.name

    for pattern in ignore_patterns:
        # Handle directory-specific patterns (e.g., dir/*)
        if "/" in pattern:
            # Convert the pattern to a relative path pattern
            if fnmatch.fnmatch(str(file_path), pattern):
                return True
        # Handle simple file patterns
        elif fnmatch.fnmatch(file_name, pattern):
            return True

    return False


def scan_directory(directory_path):
    """Scan a directory and return metadata for all files, respecting .gitignore patterns."""
    all_files_metadata = []

    # Load all gitignore patterns from the directory and its parents
    ignore_patterns = load_gitignore_patterns(directory_path)

    for root, _, files in os.walk(directory_path):
        # Load additional gitignore patterns from this subdirectory
        subdir_patterns = load_gitignore_patterns(root)
        all_patterns = ignore_patterns + subdir_patterns

        for filename in files:
            # Skip .gitignore files themselves
            if filename == ".gitignore":
                continue

            file_path = os.path.join(root, filename)

            # Skip files that match gitignore patterns
            if should_ignore(file_path, all_patterns):
                continue

            try:
                metadata = get_file_metadata(file_path)
                all_files_metadata.append(metadata)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return all_files_metadata


def main():
    # Determine user's home directory based on platform
    if platform.system() == "Windows":
        home_dir = os.path.expanduser("~")
        downloads_dir = os.path.join(home_dir, "Downloads")
        desktop_dir = os.path.join(home_dir, "Desktop")
    elif platform.system() == "Darwin":  # macOS
        home_dir = os.path.expanduser("~")
        downloads_dir = os.path.join(home_dir, "Downloads")
        desktop_dir = os.path.join(home_dir, "Desktop")
    else:  # Linux and others
        home_dir = os.path.expanduser("~")
        downloads_dir = os.path.join(home_dir, "Downloads")
        desktop_dir = os.path.join(home_dir, "Desktop")

    # Scan directories
    print("Scanning Downloads folder...")
    downloads_metadata = scan_directory(downloads_dir)

    print("Scanning Desktop folder...")
    desktop_metadata = scan_directory(desktop_dir)

    # Combine metadata
    all_metadata = downloads_metadata + desktop_metadata

    if not all_metadata:
        print("No files found.")
        return

    # Create output directory if it doesn't exist
    output_dir = os.path.join(home_dir, "FileMetadata")
    os.makedirs(output_dir, exist_ok=True)

    # Write metadata to CSV
    csv_path = "/Users/omkar/Desktop/ManagementSystems/oms/UtilityArea/FileOrg/fileMetadata.csv"

    # Get all possible field names from the metadata
    fieldnames = set()
    for item in all_metadata:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_metadata)

    print(f"Metadata for {len(all_metadata)} files saved to {csv_path}")


if __name__ == "__main__":
    main()
