import os
import json
from pathlib import Path
from typing import Tuple

from outpost_d import config
from src.models import Canonical, Basic, Social, Advanced, Upload


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
        def canonical(path: Path, entry_id: str) -> Canonical:
            """
            Read the canonical entry from a JSON file.
            The file is expected to be in the specified path.
            """
            project_dir = path / entry_id
            canon_path = project_dir / "canonical.json"
            if not canon_path.exists():
                raise CacheError(f"File {canon_path} does not exist.")

            with open(canon_path, 'r') as f:
                try:
                    canon_data = json.load(f)
                except json.JSONDecodeError:
                    raise CacheError(f"File {canon_path} is not a valid JSON file.")
                try:
                    return Canonical(**canon_data)
                except TypeError:
                    raise CacheError(f"Invalid entry format for {entry_id}.")

        @staticmethod
        def site_map(
            root_path: str = config.CANON,
            canon_file_name: str = config.SITE_MAP
            ) -> dict[str, Canonical]:
            """
            Read the site map from a JSON file.
            The file is expected to be in the specified root path.
            """
            canon_path = Path(root_path) / canon_file_name

            if not canon_path.exists():
                raise CacheError(f"File {canon_path} does not exist.")

            with open(canon_path, 'r') as f:
                try:
                    canon_data = json.load(f)
                except json.JSONDecodeError:
                    raise CacheError(f"File {canon_path} is not a valid JSON file.")

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
        def metadata(path: Path, entry_id: str) -> Tuple[Basic, Social, Advanced, Upload]:
            """
            Read the metadata from JSON files.
            The files are expected to be in the specified path.
            """
            project_dir = path / entry_id
            if not project_dir.exists():
                raise CacheError(f"Directory {project_dir} does not exist.")

            metadata = []
            for meta_type in ['basic', 'social', 'advanced', 'upload']:
                meta_path = project_dir / f"{meta_type}.json"
                if not meta_path.exists():
                    raise CacheError(f"File {meta_path} does not exist.")
                with open(meta_path, 'r') as f:
                    try:
                        metadata.append(json.load(f))
                    except json.JSONDecodeError:
                        raise CacheError(f"File {meta_path} is not a valid JSON file.")
            return tuple(metadata)


        @staticmethod
        def metadata_map(site_map: dict[str, Canonical], path: Path) -> dict[str, Tuple[Basic, Social, Advanced, Upload]]:
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
        def canonical(
                entry: Canonical,
                root_path: str = config.CANON,
                working_dir: str = config.WORKING
                ) -> None:
            """
            Write the canonical entry to a JSON file.
            The file is saved in the specified root path and working directory.
            """
            project_dir = Path(root_path) / working_dir / entry.id
            if not project_dir.exists():
                os.makedirs(project_dir, exist_ok=True)
            canon_path = project_dir / "canonical.json"
            with open(canon_path, 'w') as f:
                json.dump(entry.__dict__, f, indent=4)

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
                meta: Tuple[Basic, Social, Advanced, Upload],
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

            for meta_type, meta_data in zip(['basic', 'social', 'advanced', 'upload'], meta):
                meta_path = project_dir / f"{meta_type}.json"
                with open(meta_path, 'w') as f:
                    json.dump(meta_data, f, indent=4)

        @staticmethod
        def metadata_map(
                metadata_map: dict[str, Tuple[Basic, Social, Advanced, Upload]],
                root_path: str = config.CANON,
                working_dir: str = config.WORKING
                ) -> None:
            """
            Write the metadata map to JSON files.
            The files are saved in the specified root path and working directory.
            """
            for entry_id, meta in metadata_map.items():
                FileIO.Write.metadata(entry_id, meta, root_path, working_dir)


    @staticmethod
    def read():
        """
        Return the FileIO.Read class.
        This class contains methods for reading data from JSON files.
        """
        return FileIO.Read

    @staticmethod
    def write():
        """
        Return the FileIO.Write class.
        This class contains methods for writing data to JSON files.
        """
        return FileIO.Write


class classproperty:
    """ Decorator to define a class property."""
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, _, owner):
        return self.fget(owner)


SITE_MAP: dict[str, Canonical] = {}
METADATA_MAP: dict[str, tuple[Basic, Social, Advanced, Upload]] = {}
PROJECT: Canonical | None = None
FRAGMENTS: dict[str, str] = {}


class Cache:

    @classproperty
    def fragment(cls) -> str:
        entry = Cache.project
        frag = FRAGMENTS.get(entry.id, "")
        if not frag:
            frag = FileIO.Read.fragment(entry.id)
            FRAGMENTS[entry.id] = frag
        return frag


    @classproperty
    def site_map(cls) -> dict[str, Canonical]:
        """
        Return the current site map.
        The site map is a dictionary mapping entry IDs to their corresponding
        Canonical objects.
        """
        return SITE_MAP

    @classproperty
    def metadata_map(cls) -> dict[str, tuple[Basic, Social, Advanced, Upload]]:
        """
        Return the current metadata map.
        The metadata map is a dictionary mapping entry IDs to tuples of Basic,
        Social, Advanced, and Upload objects.
        """
        return METADATA_MAP

    @staticmethod
    def checkout(key: str) -> Canonical:
        """
        Switch the current project to the one with the given ID.
        If the ID does not exist in the cache, raise a CacheError.
        """
        global PROJECT
        if key not in SITE_MAP:
            raise CacheError(f"Entry {key} does not exist.")
        PROJECT = SITE_MAP[key]
        return Cache.project


    @classproperty
    def project(cls) -> Canonical | None:
        """
        Return the current project.
        The project is a Canonical object representing the current project.
        If no project is set, return None.
        """
        return PROJECT

    @classproperty
    def metadata(cls) -> tuple[Basic, Social, Advanced, Upload] | tuple[None, None, None, None]:
        """
        Return the current metadata.
        The metadata is a dictionary mapping entry IDs to tuples of Basic,
        Social, Advanced, and Upload objects.
        """
        if Cache.project is None:
            return (None, None, None, None)
        return METADATA_MAP[Cache.project.id]

    @staticmethod
    def add(entry: Canonical) -> None:
        """
        Add a new entry to the cache.
        If the entry already exists, raise a CacheError.
        """
        global SITE_MAP
        if entry.id in SITE_MAP:
            raise CacheError(f"Entry {id} already exists.")
        SITE_MAP[entry.id] = entry

    @staticmethod
    def update(entry: Canonical) -> None:
        """
        Update the current project with the given entry.
        If the entry does not exist in the cache, raise a CacheError.
        """
        global SITE_MAP

        if entry.id not in SITE_MAP:
            raise CacheError(f"Entry {entry.id} does not exist.")
        if Cache.project.id != entry.id:
            raise CacheError(f"Entry {entry.id} does not match the current project.")
        SITE_MAP[entry.id] = entry

    @staticmethod
    def delete(entry: Canonical) -> None:
        """
        Delete the current project from the cache.
        If the project is not in the cache, raise a CacheError.
        If the project is the current project, set PROJECT to None.
        """
        global SITE_MAP
        if entry.id not in SITE_MAP:
            raise CacheError(f"Entry {entry.id} does not exist.")
        if Cache.project.id == entry.id:
            raise CacheError(f"Entry {entry.id} is the current project.")
        del SITE_MAP[entry.id]


