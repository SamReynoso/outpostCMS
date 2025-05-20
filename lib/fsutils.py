import os
import json
from pathlib import Path

def does_not_exist(path):
    """ Check if a file or directory does not exist at the given path. """
    if os.path.exists(path):
        return False
    return True


def mkdir(path: Path, exist_ok=True):
    """
    Create a directory at the given path. If the directory already exists and
    exist_ok is False, raise a FileExistsError.
    """
    if not exist_ok and os.path.exists(path):
        raise FileExistsError(f"Directory {path} already exists.")
    os.makedirs(path, exist_ok=exist_ok)


def write(file_path, content):
    """ Write content to a file at the given path. If the file already exists """
    with open(file_path, 'w') as f:
        f.write(content)


def touch_json(path: Path, file_name: str, content: dict | list, indent=4):
    """
    Create a JSON file with the given content. If the file already exists,
    overwrite it.
    """
    file_path = Path(path) /  file_name
    write(file_path, json.dumps(content, indent=indent))


def cp(src, dst, r=False):
    """
    Copy a file or directory from src to dst. If src is a directory, dst must
    be a directory and r must be True. If src is a file, dst can be a file or
    directory.
    """
    if os.path.isdir(src):
        if not r:
            raise ValueError("Recursive copy is required for directories.")
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                cp(s, d)
            else:
                write(d, open(s).read())
    else:
        write(dst, open(src).read())
