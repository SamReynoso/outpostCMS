import os
import json
from pathlib import Path
from typing import Tuple

from outpost_d import config
from lib import git
from src.models import Canonical, Basic, Social, Advanced 


class CacheError(Exception):
    """Custom exception for cache errors."""
    def __init__(self, message: str):
        super().__init__(message)



class FileIO:
    class Read:

        @staticmethod
        def fragment(path: Path, entry_id: str) -> str:
            """
            Read the fragment from a JSON file.
            The file is expected to be in the specified path.
            """
            fragment_path = path / entry_id / "index.html"
            if not fragment_path.exists():
                raise CacheError(f"File {fragment_path} does not exist.")

            with open(fragment_path, 'r') as f:
                try:
                    return f.read()
                except Exception as e:
                    raise CacheError(f"Error reading file {fragment_path}: {e}")


        @staticmethod
        def site_map(
            root_path: str = config.CANON,
            site_map_file_name: str = config.SITE_MAP
            ) -> dict[str, Canonical]:
            """
            Read the site map from a JSON file.
            The file is expected to be in the specified root path.
            """
            site_map_path = Path(root_path) / site_map_file_name 

            if not site_map_path.exists():
                raise CacheError(f"Site map file '{site_map_path}' does not exist.")

            with open(site_map_path, 'r') as f:
                try:
                    canon_data = json.load(f)
                except json.JSONDecodeError:
                    raise CacheError(f"Site map file {site_map_path} is not a valid JSON file.")

            temp = {}
            for key, value in canon_data.items():
                if isinstance(value, dict):
                    try:
                        entry = Canonical(**value)
                        if key != entry.id:
                            raise CacheError(f"ID mismatch: {key} != {entry.id}")
                        temp[entry.id] = entry
                    except TypeError:
                        raise CacheError(f"Invalid entry format for {key}.")
                else:
                    raise CacheError(f"Invalid entry format for {key}.")
            return temp


        @staticmethod
        def metadata(path: Path, entry_id: str) -> Tuple[Basic, Social, Advanced]:
            """
            Read the metadata from JSON files.
            The files are expected to be in the specified path.
            """
            project_dir = path / entry_id
            if not project_dir.exists():
                raise CacheError(f"Directory {project_dir} does not exist.")

            metadata = []
            for meta_type in ['basic', 'social', 'advanced']:
                meta_path = project_dir / f"{meta_type}.json"
                if not meta_path.exists():
                    raise CacheError(f"File {meta_path} does not exist.")
                with open(meta_path, 'r') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        raise CacheError(f"File {meta_path} is not a valid JSON file.")

                    try:
                        if meta_type == 'basic':
                            metadata.append(Basic(**data))
                        elif meta_type == 'social':
                            metadata.append(Social(**data))
                        elif meta_type == 'advanced':
                            metadata.append(Advanced(**data))
                        else:
                            raise CacheError(f"Unknown metadata type: {meta_type}")
                    except TypeError:
                        raise CacheError(f"Invalid metadata format for {meta_type}.")
            return tuple(metadata)


        @staticmethod
        def metadata_map(site_map: dict[str, Canonical], path: Path) -> dict[str, Tuple[Basic, Social, Advanced]]:
            """
            Read the metadata map from JSON files.
            The files are expected to be in the specified path.
            """
            return {
                entry.id: FileIO.Read.metadata(path, entry.id)
                for entry in site_map.values()
            }


    class Write:

        @staticmethod
        def site_map(
                site_map: dict[str, Canonical],
                root_path: str = config.CANON,
                site_map_file_name: str = config.SITE_MAP
                ) -> None:
            """
            Write the site map to a JSON file.
            The file is saved in the specified root path.
            """
            canon_path = Path(root_path) / site_map_file_name
            temp = {
                entry.id: entry.__dict__ for entry in site_map.values()
            }
            with open(canon_path, 'w') as f:
                json.dump(temp, f, indent=4)

        @staticmethod
        def metadata(
                entry_id: str,
                meta: Tuple[Basic, Social, Advanced],
                root_path: str = config.CANON,
                working_dir: str = config.WORKING
                ) -> None:
            """
            Write the metadata to JSON files.
            The files are saved in the specified root path and working directory.
            """
            project_dir = Path(root_path) / working_dir / entry_id
            if not project_dir.exists():
                os.makedirs(project_dir, exist_ok=True)

            for meta_type, metadata in zip(['basic', 'social', 'advanced'], meta):
                meta_path = project_dir / f"{meta_type}.json"
                with open(meta_path, 'w') as f:
                    f.write(metadata.model_dump_json(indent=4))
                    

        @staticmethod
        def metadata_map(
                metadata_map: dict[str, Tuple[Basic, Social, Advanced]],
                root_path: str = config.CANON,
                working_dir: str = config.WORKING
                ) -> None:
            """
            Write the metadata map to JSON files.
            The files are saved in the specified root path and working directory.
            """
            for entry_id, meta in metadata_map.items():
                FileIO.Write.metadata(entry_id, meta, root_path, working_dir)



class classproperty:
    """ Decorator to define a class property."""
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, _, owner):
        return self.fget(owner)


SITE_MAP: dict[str, Canonical] = {}
METADATA_MAP: dict[str, tuple[Basic, Social, Advanced]] = {}
FRAGMENTS: dict[str, str] = {}


class Cache:

    @classproperty
    def canon(cls) -> Canonical | None:
        """
        Return the current project.
        The project is a Canonical object representing the current project.
        If no project is set, return None.
        """
        branch, ret = git.branch_name(Path(config.CANON) / config.WORKING)
        if ret is False:
            raise CacheError(f"Error getting branch name: {branch}")
        if branch == config.WORKING:
            print(f"[INFO] No project set, using working branch.")
            return None
        if branch not in Cache.site_map:
            raise CacheError(f"Entry {branch} does not exist.")
        return Cache.site_map[branch]

    @staticmethod
    def canon_by_id(canon_id: str) -> Canonical | None:
        """
        Return the current project by ID.
        The project is a Canonical object representing the current project.
        If no project is set, return None.
        """
        if canon_id not in Cache.site_map:
            raise CacheError(f"Entry {canon_id} does not exist.")
        return Cache.site_map[canon_id]

#    @classproperty
#    def working(cls) -> Canonical | None:
#        """
#        Return the current working project.
#        The project is a Canonical object representing the current project.
#        If no project is set, return None.
#        """
#        branch, ret = git.branch_name(Path(config.CANON) / config.WORKING)
#        if ret is False:
#            raise CacheError(f"Error getting branch name: {branch}")
#        if branch == config.WORKING:
#            print(f"[INFO] No project set, using working branch.")
#            return None
#        return Cache.site_map[branch]

    @classproperty
    def metadata(cls) -> tuple[Basic, Social, Advanced]:
        """
        Return the current metadata.
        The metadata is a dictionary mapping entry IDs to tuples of Basic,
        Social, Advanced, and Upload objects.
        """
        if Cache.canon is None:
            raise CacheError("No project is set.")
        global METADATA_MAP
        if Cache.canon.id not in METADATA_MAP:
            METADATA_MAP[Cache.canon.id] = FileIO.Read.metadata(
                Path(config.CANON) / config.WORKING,
                Cache.canon.id
            )
        return METADATA_MAP[Cache.canon.id]

    @staticmethod
    def metadata_by_id(id) -> tuple[Basic, Social, Advanced]:
        """
        Return the current metadata.
        The metadata is a dictionary mapping entry IDs to tuples of Basic,
        Social, Advanced, and Upload objects.
        """
        global METADATA_MAP
        if id not in METADATA_MAP:
            METADATA_MAP[id] = FileIO.Read.metadata(
                Path(config.CANON) / config.WORKING,
                id
            )
        return METADATA_MAP[id]

    @classproperty
    def fragment(cls) -> str:
        """
        Return the current fragment.
        The fragment is a string representing the current project.
        If no project is set, raise a CacheError.
        """
        canon = Cache.canon
        frag = FRAGMENTS.get(canon.id, "")
        if not frag:
            frag = FileIO.Read.fragment(
                Path(config.CANON) / config.WORKING,
                canon.id
            )
            FRAGMENTS[canon.id] = frag
        return frag


    @staticmethod
    def fragment_by_id(id) -> str:
        """
        Return the current fragment.
        The fragment is a string representing the current project.
        If no project is set, raise a CacheError.
        """
        frag = FRAGMENTS.get(id, "")
        if not frag:
            frag = FileIO.Read.fragment(
                Path(config.CANON) / config.WORKING,
                id
            )
            FRAGMENTS[id] = frag
        return frag

    @classproperty
    def site_map(cls) -> dict[str, Canonical]:
        """
        Return the current site map.
        The site map is a dictionary mapping entry IDs to their corresponding
        Canonical objects.
        """
        global SITE_MAP
        if not SITE_MAP or SITE_MAP == {}:
            SITE_MAP = FileIO.Read.site_map()
        return SITE_MAP

    @classproperty
    def metadata_map(cls) -> dict[str, tuple[Basic, Social, Advanced]]:
        """
        Return the current metadata map.
        The metadata map is a dictionary mapping entry IDs to tuples of Basic,
        Social, Advanced, and Upload objects.
        """
        return METADATA_MAP


    @staticmethod
    def add(canon: Canonical) -> None:
        """
        Add a new entry to the cache.
        If the entry already exists, raise a CacheError.
        """
        global SITE_MAP, CANON
        if canon.id in Cache.site_map:
            raise CacheError(f"Entry {id} already exists.")
        SITE_MAP[canon.id] = canon

    @staticmethod
    def update_metadata(metadata: tuple[Basic, Social, Advanced]) -> None:
        """
        Update the metadata for the current project.
        If the project is not in the cache, raise a CacheError.
        """
        global METADATA_MAP
        entry = Cache.canon
        if entry is None:
            raise CacheError("No project is set.")
        METADATA_MAP[entry.id] = metadata

    @staticmethod
    def update_canonical(canon: Canonical) -> None:
        """
        Update the current project with the given entry.
        If the entry does not exist in the cache, raise a CacheError.
        """
        global SITE_MAP


        if canon.id not in Cache.site_map:
            raise CacheError(f"Entry {canon.id} does not exist.")
        # This hasn't happened yet, but if it does, we need to raise an error
        if canon.hash is None:
            raise CacheError("No project is set.")
        SITE_MAP[canon.id] = canon 

    @staticmethod
    def delete_canonical() -> None:
        """
        Delete the current project from the cache.
        If the project is not in the cache, raise a CacheError.
        If the project is the current project, set CANON to None.
        """
        global SITE_MAP
        canon = Cache.canon
        if canon.id not in Cache.site_map:
            raise CacheError(f"Entry {canon.id} does not exist.")
        del SITE_MAP[canon.id]

    @staticmethod
    def delete_metadata() -> None:
        """
        Delete the metadata for the current project.
        If the project is not in the cache, raise a CacheError.
        """
        global METADATA_MAP
        canon = Cache.canon
        if canon.id not in Cache.metadata_map:
            raise CacheError(f"Entry {canon.id} does not exist.")
        del METADATA_MAP[canon.id]


