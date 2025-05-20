from datetime import datetime
from pathlib import Path

from outpost_d import config
from src.models import Canonical, Basic, Social, Advanced 
from lib.locached import FileIO, CacheError


class classproperty:
    """ Decorator to define a class property."""
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, _, owner):
        return self.fget(owner)


SITE_MAP: dict[str, Canonical] = {}
METADATA_MAP: dict[str, tuple[Basic, Social, Advanced]] = {}
FRAGMENTS: dict[str, str] = {}

def from_args(frunc):
    def wrapper(*args, **_):
        if len(args) == 2:
            group, project = args
            id = f"{group}/{project}"
            return frunc(id)
        return frunc(*args)
    return wrapper

class Public:
    path: Path = Path(config.CANON) / config.PUBLISH

    @staticmethod
    def groups():
        """ Returns a list of groups """
        global SITE_MAP
        if SITE_MAP == {}:
            try:
                SITE_MAP = FileIO.Read.site_map()
            except CacheError:
                return []
        groups = set()
        for k in SITE_MAP.keys():
            group = k.split("/")[0]
            groups.add(group)
        return list(groups)

    @staticmethod
    def projects():
        """ Returns a list of projects """
        global SITE_MAP
        if SITE_MAP == {}:
            try:
                SITE_MAP = FileIO.Read.site_map()
            except CacheError:
                return []
        projects = set()
        for k in SITE_MAP.keys():
            projects.add(k)
        return list(projects)

    @staticmethod
    @from_args
    def canon(id: str, *_) -> Canonical | None:
        global SITE_MAP
        if SITE_MAP == {}:
            Public.site_map()
        else:
            if id not in SITE_MAP:
                try:
                    SITE_MAP = FileIO.Read.site_map()
                except CacheError:
                    return None

        canon = SITE_MAP.get(id, None)
        if canon is None:
            print(f"[DEBUG] Public.canon({id}) is None")
            return None
        if canon.public is False:
            print(f"[DEBUG] Public.canon({id}) is not public")
            return None
        return canon

    @staticmethod
    @from_args
    def pull_metadata(id) -> bool:
        global METADATA_MAP
        if id in METADATA_MAP:
            return True

        canon = Public.canon(id)
        if canon is None:
            return False
        if canon.public is False:
            return False

        if METADATA_MAP == {}:
            try:
                METADATA_MAP[id] = FileIO.Read.metadata(Public.path, id)
                return True
            except CacheError:
                return False
        else:
            if id not in METADATA_MAP:
                try:
                    METADATA_MAP[id] = FileIO.Read.metadata(Public.path, id)
                    return True
                except CacheError:
                    return False
        return True


    @staticmethod
    def meta_dump(metadata: tuple[Basic, Social, Advanced]) -> list[dict] | None:
        data = []
        for model in metadata:
            try:
                model = model.model_dump()
            except AttributeError:
                return None
            for label, value in model.items():
                if isinstance(value, datetime):
                    model[label] = value.isoformat()
            data.append(model)
        return data

    @staticmethod
    @from_args
    def metadata(id, *_) -> list[dict] | None:
        global METADATA_MAP
        if Public.canon(id) is None:
            return None
        Public.pull_metadata(id)
        data = METADATA_MAP.get(id, None)
        if data is None:
            return None
        return Public.meta_dump(data)
    
    @staticmethod
    def group_metadata(group: str) -> dict[str, list[dict]] | None:
        """ Returns a dictionary of metadata for a group """
        global METADATA_MAP
        metadata = {}
        for k, v in Public.site_map().items():
            if v.public is False:
                continue
            if k.startswith(group) is False:
                continue
            data= Public.metadata(k)
            if data is None:
                continue
            metadata[k] = data
        return metadata

    @staticmethod
    def site_metadata() -> dict[str, list[dict]] | None:
        """ Returns a dictionary of metadata for the site """
        global METADATA_MAP
        metadata = {}
        for k, v in Public.site_map().items():
            if v.public is False:
                continue
            data= Public.metadata(k)
            if data is None:
                continue
            metadata[k] = data
        return metadata

    @staticmethod
    @from_args
    def basic(id) -> Basic | None:
        metadata = Public.metadata(id)
        if metadata is None:
            return None
        return Basic(**metadata[0])


    @staticmethod
    @from_args
    def social() -> Social | None:
        metadata = Public.metadata(id)
        if metadata is None:
            return None
        return Social(**metadata[1])
    
    @staticmethod
    @from_args
    def advanced(id) -> Advanced | None:
        metadata = Public.metadata(id)
        if metadata is None:
            return None
        return Advanced(**metadata[2])

    @staticmethod
    @from_args
    def fragment(id, *_) -> str | None:
        global FRAGMENTS
        if Public.canon(id) is None:
            print(f"[DEBUG] Public.canon({id}) is None")
            return None
        if id in FRAGMENTS:
            return FRAGMENTS[id]
        try:
            FRAGMENTS[id] = FileIO.Read.fragment(Public.path, id)
            return FRAGMENTS[id]
        except CacheError:
            return None

    @staticmethod
    def site_map() -> dict[str, Canonical]:
        global SITE_MAP
        if SITE_MAP == {}:
            try:
                SITE_MAP = FileIO.Read.site_map()
            except CacheError:
                pass
        return SITE_MAP

    
    @staticmethod
    def group_fragments(group: str) -> dict[str, str] | None:
        """ Returns a dictionary of fragments for a group """
        global FRAGMENTS
        fragments = {}
        for k, v in Public.site_map().items():
            if v.public is True:
                if k.startswith(group):
                    fragments[k] = Public.fragment(k)
        return fragments

    @staticmethod
    def site_fragments() -> dict[str, str] | None:
        """ Returns a dictionary of fragments for the site """
        global FRAGMENTS
        fragments = {}
        for k, v in Public.site_map().items():
            if v.public is True:
                fragments[k] = Public.fragment(k)
        return fragments

