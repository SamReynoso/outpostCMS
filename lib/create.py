from lib.fsutils import (
        new_article_entry,
        write_articles_json,
        create_project_dir,
        new_metadata,
        write_metadata_json,
        )
from lib.loadsite import get_articles_json
import config


def create_project(group, project_name, canonical):
    content = config.CONTENT_DIR
    meta = new_metadata()
    
    project_dir = create_project_dir(content, group, project_name)
    write_metadata_json(project_dir, meta)

    new_entry = new_article_entry(group, project_name, canonical)
    articles = get_articles_json()
    articles.append(new_entry)
    write_articles_json(config.CANONICAL_DIR, articles) 

