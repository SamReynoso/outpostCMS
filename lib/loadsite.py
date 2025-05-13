import time
import json
from pathlib import Path
import sys

import config
from fastapi import HTTPException

SITE_MAP = []
CANONICAL_INDEX = {}
LAST_LOAD = 0



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
    def update_on_interval():
        global LAST_LOAD
        uptime = time.time() - LAST_LOAD
        if uptime > config.CACHE_DELAY:
            Cache.update_now()

    @staticmethod
    def update_article_index():
        global SITE_MAP, CANONICAL_INDEX
        CANONICAL_INDEX = {
                entry['canonical']: load_article_metadata(entry) for entry in SITE_MAP
                }

    @staticmethod
    def update_now():
        global LAST_LOAD, SITE_META, CANONICAL_INDEX
        SITE_META = load_valid_site_map()
        LAST_LOAD = time.time()
        Cache.update_article_index()

    @staticmethod
    def get(canonical):
        global CANONICAL_INDEX
        if CANONICAL_INDEX.__len__() == 0:
            Cache.update_now()
        entry = CANONICAL_INDEX.get(canonical)
        if not entry:
            print(f"[ERROR] Entry not found in canonical index: {canonical}")
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry

    @staticmethod
    def site_map():
        global SITE_META
        if SITE_META.__len__() == 0:
            Cache.update_now()
        return SITE_META

def load_fragment(metadata) -> str:
    if not metadata:
        print("[ERROR] Metadata is None or empty")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    content_dir = metadata.get('path')
    if not content_dir:
        print("[ERROR] Content directory is None or empty")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    fragment_path = Path(content_dir) / "index.html"
    if not fragment_path.is_file():
        print(f"[ERROR] File for fragment not found: {fragment_path}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    try:
        with open(fragment_path) as fragment_file:
            return fragment_file.read()
    except IOError:
        print(f"[ERROR] Error reading fragment file: {fragment_path}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def load_article_metadata(entry: dict) -> dict:
    content_dir = entry.get('path')
    if not content_dir:
        print("[ERROR] Content directory is None or empty")
        return {}
    meta_path = Path(content_dir) / "meta.json"
    if not meta_path.is_file():
        print(f"[ERROR] Meta file not found: {meta_path}")
        return {}
    try:
        with open(meta_path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[ERROR] Error decoding JSON from meta file: {meta_path}")
        return {}
    except IOError:
        print(f"[ERROR] Error reading meta file: {meta_path}")
        return {}

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


