import os
import argparse

def combine_py_files(root_dir, output_file, exclude_dirs=None):
    """
    Combines all Python files in a directory tree into a single text file
    with full relative paths in headers, excluding specified directories.
    """
    exclude_dirs = set(exclude_dirs or [])

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(root_dir):
            # Modify dirs in-place to skip excluded folders
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            rel_path = os.path.relpath(file_path, root_dir)
                            header = f"\n\n{'#' * 40}\n# {rel_path}\n{'#' * 40}\n\n"
                            outfile.write(header)
                            outfile.write(infile.read())
                        print(f"Added: {rel_path}")
                    except Exception as e:
                        print(f"Error reading {rel_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine Python files into a single text file with paths')
    parser.add_argument('-i', '--input', default='.', help='Input directory (default: current)')
    parser.add_argument('-o', '--output', default='combined.txt', help='Output file (default: combined.txt)')
    parser.add_argument('-x', '--exclude', nargs='*', default=['venv','__pycache__','__init__.py'], help='Folders to exclude (e.g. venv __pycache__)')

    args = parser.parse_args()

    combine_py_files(os.path.normpath(args.input), args.output, args.exclude)
    print(f"\nCombined file created: {args.output}")
