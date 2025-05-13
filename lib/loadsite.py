import json
from pathlib import Path
import sys


def log_error(msg, entry):
    print(f"[ERROR] {msg} (canonical: {entry.get('canonical', '?')})", file=sys.stderr)


def load_article_json(site_entry: dict) -> dict:
    content_dir = site_entry['path']
    meta_path = Path(content_dir) / "meta.json"
    with open(meta_path) as f:
        return json.load(f)

def load_and_validate_site_data(json_path='canonical/articles.json'):

    with open(json_path, 'r') as f:
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
        try:
            article = load_article_json(entry)
        except Exception as e:
            log_error(f"Error loading meta.json: {e}", entry)
            continue
        if not isinstance(article, dict):
            log_error("Invalid article JSON format", entry)
            continue
        if not article.get('title'):
            log_error("Missing title in article JSON", entry)
            continue
        if not article.get('date'):
            log_error("Missing date in article JSON", entry)
            continue

        article['canonical'] = canonical_str
        article['path'] = content_dir
        article['public'] = public

        valid_entries.append(article)

    return valid_entries


def load_everything():
    with open('canonical/articles.json', 'r') as f:
        data = json.load(f)

    valid_entries = []

    for entry in data:
        article = {}
        content_dir = entry.get('path')
        if content_dir is not None:
            try:
                article = load_article_json(entry)
            except Exception as e:
                log_error(f"Error loading meta.json: {e}", entry)
            article['canonical'] = entry.get('canonical')
            article['path'] = content_dir
            article['public'] = entry.get('public', False)

        valid_entries.append(article)
    return valid_entries


if __name__ == "__main__":
    data = load_and_validate_site_data()
    print(f"loaded {len(data)} valid entries")
