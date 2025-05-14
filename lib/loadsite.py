import time
import json
from pathlib import Path
import sys

import config
from fastapi import HTTPException


def log_error(msg, entry):
    print(f"[ERROR] {msg} (canonical: {entry.get('canonical', '?')})", file=sys.stderr)


def get_articles_json():
    ARTICLES_JSON = Path(config.CANONICAL_DIR) / "articles.json"
    if ARTICLES_JSON.exists():
        with open(ARTICLES_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []



class Cache:

    @staticmethod
    def site_map():
        return  load_zip_map()

    @staticmethod
    def indexed_site_map():
        def format_path(entry):
            return entry['group'] + '/' + entry['project_name'] 
        site_map = Cache.site_map()
        indexed_map = { format_path(entry): entry for entry in site_map }
        return indexed_map

    @staticmethod
    def get_project(group, project_name):
        indexed_map = Cache.indexed_site_map()
        key = group + '/' + project_name
        if key in indexed_map:
            return indexed_map[key]
        else:
            return None





def load_fragment(group, project_name) -> str:
    fragment_path = Path(config.CONTENT_DIR) / group / project_name / "index.html"
    if not fragment_path.is_file():
        print(f"[ERROR] File for fragment not found: {fragment_path}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    try:
        with open(fragment_path) as fragment_file:
            return fragment_file.read()
    except IOError:
        print(f"[ERROR] Error reading fragment file: {fragment_path}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def load_meta(group: str, project_name: str) -> dict:
    meta_path = Path(config.CONTENT_DIR) / group / project_name / "meta.json"
    if not meta_path.is_file():
        print(f"[ERROR] Meta file not found: {meta_path}")
        return {}
    try:
        with open(meta_path) as f:
            return json.load(f)
    except IOError:
        print(f"[ERROR] Error reading meta file: {meta_path}")
        return {}


def load_site_map():
    file_path = Path(config.CANONICAL_DIR) / "articles.json"
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def load_from_site_map(entry: dict) -> dict:
    project_dir = Path(config.CONTENT_DIR) / entry['group'] / entry['project_name']
    meta_path = project_dir / "meta.json"
    if not meta_path.is_file():
        print(f"[ERROR] Meta file not found: {meta_path}")
        return {}
    try:
        with open(meta_path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[ERROR] Error decoding JSON from meta file: {meta_path}")
        return {}

def load_zip_map():
    site_map = load_site_map()
    zip = []
    for entry in site_map:
        meta = load_from_site_map(entry)
        for key, value in entry.items():
            meta[key] = value
        zip.append(meta)
    return zip


def load_valid_site_map():
    file_path = Path(config.CANONICAL_DIR) / "articles.json"

    with open(file_path, 'r') as f:
        data = json.load(f)

    seen = set()
    valid_entries = []

    for entry in data:
        canonical_str = entry.get('canonical')
        content_dir = entry.get('path')
        public = entry.get('public')

        if not isinstance(canonical_str, str): 
            log_error("Invalid or missing canonical value", entry)
            continue
        if not isinstance(content_dir, str):
            log_error("Invalid or missing path value", entry)
            continue
        if not isinstance(public, bool):
            log_error("Invalid or missing public value", entry)
            continue
        if canonical_str in seen:
            log_error("Duplicate canonical value", entry)
            continue

        content = Path(content_dir)

        if not content.is_dir():
            log_error(f"Not a directory: {content_dir}", entry)
            continue
        if not content.joinpath('index.html').is_file():
            log_error("Missing index.html", entry)
            continue
        if not content.joinpath('meta.json').is_file():
            log_error("Missing meta.json", entry)
            continue
        if not public:
            print(f"[WARNING] Not public: {content_dir} (canonical: {canonical_str})", file=sys.stderr)
            continue

        valid_entries.append(entry)

    return valid_entries


