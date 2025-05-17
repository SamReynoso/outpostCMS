import json
from pathlib import Path

from outpost_d import config


def load_fragment(group, project_name) -> str:
    fragment_path = Path(config.CANON) / config.WORKING / group / project_name / "index.html"
    with open(fragment_path) as fragment_file:
        return fragment_file.read()


def load_meta(group: str, project_name: str) -> dict:
    meta_path = Path(config.CANON) / config.WORKING / group / project_name / "meta.json"
    with open(meta_path) as f:
        return json.load(f)


def load_site_map():
    path = Path(config.CANON) / config.SITE_MAP
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def load_from_project(entry: dict) -> dict:
    meta_path = Path(config.CANON) / config.WORKING / format_branch(**entry) / "meta.json"
    with open(meta_path) as f:
        return json.load(f)


def load_zip_map():
    site_map = load_site_map()
    zip = []
    for entry in site_map:
        meta = load_from_project(entry)
        for key, value in entry.items():
            meta[key] = value
        zip.append(meta)
    return zip
