import os


def get_basename_from_path(file_path: str):
    return os.path.basename(file_path).split('.')[0]
