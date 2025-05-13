import json
from pathlib import Path


def create_project_dir(group: str, project_name: str):
    group_dir = Path(group) / project_name
    group_dir.mkdir(parents=True, exist_ok=True)


def new_article_entry(group: str, project_name: str, canonical: str):
    return {
        "group": group.strip(),
        "project_name": project_name.strip(),
        "canonical": canonical.strip(),
        "public": False,
    }


def new_metadata_json(group: str, project_name: str):
    metadata_json = Path("content") / group / project_name / "meta.json"
    metadata_json.touch(exist_ok=True)
    meta = {
            "title": "Untitled",
            "description": "",
            "keywords": "",
            "author": "",
            "date": "",
            "last_updated": "",

            }
    return meta

def write_metadata_json(meta, group, project_name):
    metadata_json = Path("content") / group / project_name / "meta.json"
    metadata_json.touch(exist_ok=True)
    with open(metadata_json, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=4)



def write_articles_json(articles):
    articles_json = Path("canonical/articles.json")
    articles_json.parent.mkdir(parents=True, exist_ok=True)
    with open(articles_json, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)


def create_index_html_file(group: str, project_name: str):
    index_html = Path("content") /group / project_name / "index.html"
    index_html.touch(exist_ok=True)


def upload_index_html_file(group: str, project_name: str, file):
    group_dir = Path("content") / group / project_name
    group_dir.mkdir(parents=True, exist_ok=True)
    index_html = group_dir / "index.html"
    with open(index_html, "wb") as f:
        f.write(file.file.read())
