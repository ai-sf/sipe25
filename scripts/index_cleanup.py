import os
import argparse

def cleanup_index_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Match files starting with "index" and ending with ".html"
            if filename.startswith("index") and filename.endswith(".html"):
                # Skip the exact "index.html" file
                if filename == "index.html":
                    continue
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f"Removed {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Remove index*.html files except index.html")
    parser.add_argument("root_dir", help="Root directory to clean up")
    args = parser.parse_args()
    
    cleanup_index_files(args.root_dir)

if __name__ == "__main__":
    main()
