import json
from pathlib import Path


def create_project_dir(path: str, group: str, project_name: str):
    project_dir= Path(path)/ group / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    index_html = project_dir / "index.html"
    index_html.touch(exist_ok=True)
    metadata_json = project_dir / "meta.json"
    metadata_json.touch(exist_ok=True)
    return project_dir


def write_json_file(path, json_data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)


def upload_index_html_file(path: str, group: str, project_name: str, file):
    group_dir = Path(path) / group / project_name
    if not group_dir.exists():
        raise FileNotFoundError(f"Group directory {group_dir} does not exist.")
    index_html = group_dir / "index.html"
    with open(index_html, "wb") as f:
        f.write(file.file.read())
