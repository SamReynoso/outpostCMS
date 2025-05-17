from pathlib import Path

from lib.fsutils import touch_json

import config
from lib.locached import Cache
from templates.python import new_site_map_entry, new_metadata
from lib.fsutils import mkdir, touch_json
from lib import git

def add_hash_to_metadata(path, metadata):
    hash = git.hash(path)
    metadata['hash'] = hash

def update_site_map(path, file_name, entry):
    site_map = Cache.get_site_map()
    site_map.append(entry)
    touch_json(path, file_name, site_map)

def write_metadata(path, group, project_name, metadata):
    project_directory = path  /  "foo"
    touch_json(project_directory, 'meta.json', metadata)


def create_project_directory(path, group, project_name):
    group_dir = Path(path) / group
    project_dir = group_dir / project_name
    if not group_dir.exists():
        mkdir(group_dir)
    if project_dir.exists():
        raise FileExistsError(f"Project directory {project_dir} already exists.")
    mkdir(project_dir)


def create_project(path, group, project_name, canonical):
    git.new_branch(path, fo
    create_project_directory(path, group, project_name)
    metadata = new_metadata()
    add_hash_to_metadata(path, metadata)
    write_metadata(path, group, project_name, metadata)
    git.save(path, f"Creating project {project_name} in group {group}")
    entry = new_site_map_entry(group, project_name, canonical)
    update_site_map(config.CANON, 'site-map.json', entry)


def upload_index_html_file(path: str, group: str, project_name: str, file):
    group_dir = Path(path) / group / project_name
    if not group_dir.exists():
        raise FileNotFoundError(f"Group directory {group_dir} does not exist.")
    index_html = group_dir / "index.html"
    with open(index_html, "wb") as f:
        f.write(file.file.read())


