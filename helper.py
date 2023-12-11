import os
import glob
import argparse
import hashlib
import json


def get_basename_from_path(file_path: str):
    """
    Extract file name from given file path, without extension.
    TODO: Account for multiple dots in a file name
    """
    return os.path.basename(file_path).split('.')[0]


def multiglob(patterns: list[str]) -> list[str]:
    """
    Glob on multiple patterns, and return a flattened array of file paths
    """
    paths = []
    nested_paths = [glob.glob(pattern) for pattern in patterns]
    for nested in nested_paths:
        for path in nested:
            paths.append(path)

    return paths


def rename_with_hash(file_patterns: list[str], record_file='rename_history.json') -> list[str]:
    """
    Also maps file hashes to their original names,
    for recovery purposes.
    Currently assumes that there is an extension, name will appear weird if no extension
    """
    rename_mapping = {}

    files = multiglob(file_patterns)
    for file_path in files:
        # Extract extension
        _, extension = os.path.splitext(file_path)

        # Get MD5 hash of file contents
        with open(file_path, 'rb') as f:
            hash = hashlib.md5(f.read()).hexdigest()

        # Create new file name using hash and extension
        print(extension)
        new_file_name = f'{hash}{extension}'
        
        # Get parent directories
        parent_folders = os.path.dirname(file_path)
        new_file_path = os.path.join(parent_folders, new_file_name)

        # Rename file
        os.rename(file_path, new_file_path)

        # Map hash to original file name
        original_file_name = os.path.basename(file_path)
        rename_mapping[hash] = original_file_name
    
    # Write mapping to file
    # Attempt to open record_file
    if not os.path.exists(record_file):
        with open(record_file, 'w') as f:
            f.write('{}')

    with open(record_file, 'r+') as f:
        existing_map = json.load(f)
        new_map = { **existing_map, **rename_mapping }
        f.seek(0)
        f.truncate()
        json.dump(new_map, f, indent=2)

    return files

def restore_original_names(file_patterns: list[str], record_file='rename_history.json') -> list[str]:
    """
    Currently assumes that there is an extension, name will appear weird if no extension
    """
    # No records to restore from
    if not os.path.exists(record_file):
        return []

    files = multiglob(file_patterns)
    
    for file in files:
        base_name = get_basename_from_path(file)
        
        hash, extension = os.path.splitext(base_name)

        # Search up the hash in rename history file
        with open(record_file, 'r') as f:
            records: dict[str, str] = json.load(f)
            original_name = records.get(hash)
            original_name_with_ext = f'{original_name}{extension}'

        # Get parent directories
        parent_folders = os.path.dirname(file)
        new_file_path = os.path.join(parent_folders, original_name_with_ext)

        # Rename file
        os.rename(file, new_file_path)
    
    return files


if __name__ == '__main__':
    functions = ['hash', 'restore']

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="function")
    hash_parser = subparsers.add_parser('hash')
    restore_parser = subparsers.add_parser('restore')
    hash_parser.add_argument('file_patterns', type=str, nargs='+')
    restore_parser.add_argument('file_patterns', type=str, nargs='+')
    args = parser.parse_args()

    if args.function == 'hash':
        file_patterns = args.file_patterns

        files = rename_with_hash(file_patterns)
    
        print(f'Processed:')

        for file in files:
            print(file)

    elif args.function == 'restore':
        file_patterns = args.file_patterns

        files = restore_original_names(file_patterns)

        print(f'Processed:')

        for file in files:
            print(file)
        