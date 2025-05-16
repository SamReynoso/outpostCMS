import json
from pathlib import Path

import config
from lib.formatters import format_branch


def get_site_map() -> list:
    site_map_path= Path(config.CANON) / config.SITE_MAP
    if site_map_path.exists():
        with open(site_map_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []


class Cache:

    @staticmethod
    def all():
        return  load_zip_map()

    @staticmethod
    def get_site_map():
        return get_site_map()

    @staticmethod
    def indexed_site_map():
        site_map = Cache.all()
        indexed_map = { format_branch(**entry): entry for entry in site_map }
        return indexed_map

    @staticmethod
    def get_project(group, project_name):
        indexed_map = Cache.indexed_site_map()
        key = format_branch(group=group, project_name=project_name)
        return indexed_map[key]



def load_fragment(group, project_name) -> str:
    fragment_path = Path(config.WORKING) / group / project_name / "index.html"
    with open(fragment_path) as fragment_file:
        return fragment_file.read()


def load_meta(group: str, project_name: str) -> dict:
    meta_path = Path(config.WORKING) / group / project_name / "meta.json"
    with open(meta_path) as f:
        return json.load(f)


def load_site_map():
    with open(config.SITE_MAP, 'r') as f:
        data = json.load(f)
    return data


def load_from_project(entry: dict) -> dict:
    meta_path = Path(config.WORKING) / format_branch(**entry) / "meta.json"
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
