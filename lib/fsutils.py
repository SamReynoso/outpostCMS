import os
import json
from pathlib import Path

def does_not_exist(path):
    if os.path.exists(path):
        print(f"Path already exists: {path}")
        raise Exception("Path already exists")
    return True



def mkdir(path):
    assert does_not_exist(path), f"Path already exists: {path}"
    print(f"[INFO] Creating directory: {path}")
    os.makedirs(path, exist_ok=False)


def write(file_path, content):
    with open(file_path, 'w') as f:
        print(f"[INFO] Creating new file: {file_path}")
        f.write(content)


def touch_json(path, file_name, content):
    file_path = Path(path) /  file_name
    write(file_path, json.dumps(content, indent=4))


