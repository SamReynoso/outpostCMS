from lib.fsutils import (
        write_json_file,
        create_project_dir,
        )

from templates.python import new_metadata, new_site_map_entry
from lib.locached import Cache
import config


def create_project(group, project_name, canonical):
    entry = new_site_map_entry(group, project_name, canonical)
    meta = new_metadata()

    # Probably need to remove this line when git creates the project
    project_dir = create_project_dir(config.WORKING, group, project_name)
    site_map = Cache.get_site_map()
    site_map.append(entry)
    
    write_json_file(project_dir / "meta.json", meta)
    write_json_file(config.SITE_MAP, site_map) 

