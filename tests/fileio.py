from lib.locached import Cache, FileIO

from src.models import Canonical
from tests import config


SITE_MAP = {
        "outpost/test-1": {
                "group": "outpost",
                "project": "test-1",
                "canonical": "https://example.com/outpost/test-1",
                "hash": "1234567890abcdef",
                "public": True,
            }
        }

def test_write_site_map():
    testing_dir = config.ROOT_PATH
    site_map = FileIO.Read.site_map(
            root_path=testing_dir,
            site_map_file_name="site-map-starting.json"
            )
    print("site_map", site_map)

    FileIO.Write.site_map(
            site_map,
            root_path=testing_dir,
            site_map_file_name="site-map-output.json"
            )




def all():
    """Run fileio tests."""
    test_write_site_map()
    print("All tests passed.")
