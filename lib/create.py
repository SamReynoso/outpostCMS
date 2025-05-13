from lib.fsutils import (
        new_article_entry,
        write_articles_json,
        create_project_dir,
        create_index_html_file,
        new_metadata_json,
        write_metadata_json,
        )
from lib.loadsite import get_articles_json


def create_project(group, project_name, canonical):
    create_project_dir(group, project_name)
    articles = get_articles_json()
    new_entry = new_article_entry(group, project_name, canonical)
    articles.append(new_entry)
    write_articles_json(articles)
    meta = new_metadata_json(group, project_name)
    write_metadata_json(meta, group, project_name)
    create_index_html_file(group, project_name)
