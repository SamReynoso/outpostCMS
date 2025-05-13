import time
import json
from pathlib import Path

def new_article_entry(group: str, project_name: str, canonical: str):
    return {
        "group": group.strip(),
        "project_name": project_name.strip(),
        "canonical": canonical.strip(),
        "public": False,
    }


def new_metadata():
    date = time.strftime("%Y-%m-%d")
    return {
            "title": "Untitled",
            "description": "",
            "keywords": "",
            "author": "",
            "date": date,
            "last_updated": date,
            }



def create_project_dir(path: str, group: str, project_name: str):
    project_dir= Path(path)/ group / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    index_html = project_dir / "index.html"
    index_html.touch(exist_ok=True)
    metadata_json = project_dir / "meta.json"
    metadata_json.touch(exist_ok=True)
    return project_dir


def write_metadata_json(path, meta):
    meta_json = Path(path) / "meta.json"
    with open(meta_json, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=4)


def write_articles_json(path, articles):
    articles_json = Path(path) / "articles.json"
    articles_json.parent.mkdir(parents=True, exist_ok=True)
    with open(articles_json, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)


def upload_index_html_file(path: str, group: str, project_name: str, file):
    group_dir = Path(path) / group / project_name
    if not group_dir.exists():
        raise FileNotFoundError(f"Group directory {group_dir} does not exist.")
    index_html = group_dir / "index.html"
    with open(index_html, "wb") as f:
        f.write(file.file.read())
