import shutil
from pathlib import Path

from outpost_d import config
from lib.locached import Cache, FileIO
from src import models


def update_metadata(model: models.OutpostModel, index: int) -> None:
    metadata = list(Cache.metadata)
    metadata[index] = model
    Cache.update_metadata(tuple(metadata))
    CacheControl.dump()


class CacheControl:
    working: Path = Path(config.CANON) / config.WORKING

    @staticmethod
    def create_project(canonical: models.Canonical):
        metadata = (
            models.Basic.new(),
            models.Social.new(),
            models.Advanced.new(),
        )
        Cache.add(canonical)
        Cache.update_metadata(metadata)
        FileIO.Write.site_map(Cache.site_map)
        CacheControl.dump()


    class Update:
        @staticmethod
        def basic(model: models.Basic):
            update_metadata(model, 0)

        @staticmethod
        def social(model: models.Social):
            update_metadata(model, 1)

        @staticmethod
        def advanced(model: models.Advanced):
            update_metadata(model, 2)

        @staticmethod
        def canonical(model: models.Canonical):
            Cache.update_canonical(model)
            FileIO.Write.site_map(Cache.site_map)

    @staticmethod
    def delete_project():
        canon = Cache.canon
        shutil.rmtree(Path(config.WORKING) / canon.id)
        Cache.delete_metadata()
        Cache.delete_canonical()
        CacheControl.dump()
            
    @staticmethod
    def dump():
        canon = Cache.canon
        metadata = Cache.metadata
        FileIO.Write.metadata(canon.id, metadata)


    @staticmethod
    def load(path: Path = Path(config.WORKING)):
        site_map = FileIO.Read.site_map()
        for entry_id in site_map.keys():
            metadata = FileIO.Read.metadata(path, entry_id)
            Cache.update_metadata(metadata)


