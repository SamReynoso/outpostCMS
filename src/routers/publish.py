from pathlib import Path

from fastapi import APIRouter, Request

from outpost_d import config
from lib.locached import Cache
from lib.response import EntryResponse 
from lib import git
from src.formatters import format_index_diff, format_meta_diff




publish_router = APIRouter()


@publish_router.get("/")
async def index(request: Request):
    resp = EntryResponse(request, "publish/index.html")
    resp.update(site_map=Cache.site_map)
    return resp.as_response()


@publish_router.get("/preview/")
async def preview(request: Request):
    resp = EntryResponse(request, "publish/preview.html")
    resp.update(
            title="Preview",
            article_fragment=Cache.fragment()
            )
    return resp.as_response()


@publish_router.get("/workbook/")
async def workbook(request: Request):
    resp = EntryResponse(request, "publish/workbook.html")
    resp.update(title="Workbook")
    return resp.as_response()


def get_html_diff(directory: Path, file: str, hash: str = "HEAD") -> str:
    """ Get the diff of a specific file """
    diff, ret = git.run_git_command(directory, 'diff', '-U10000', '--cached', hash, '--', file)
    if ret is False:
        return f"<p>Error getting diff for {file}</p>"
    if not diff:
        if file == "index.html":
            return "<pre><code><p>Index is unchanged</p></code></pre>"
        return f"<p>This file({file}) is unchanged</p>"
    if file.endswith(".html"):
        return format_index_diff(diff)
    return format_meta_diff(diff)


def get_diffs(hash: str = "HEAD") -> dict[str, str]:
    canon = Cache.canon
    working_dir = Path(config.CANON) / config.WORKING / canon.id
    git.add(working_dir)
    return {
            "index": get_html_diff(working_dir, "index.html", hash=hash),
            "basic": get_html_diff(working_dir, "basic.json", hash=hash),
            "social": get_html_diff(working_dir, "social.json", hash=hash),
            "advanced": get_html_diff(working_dir, "advanced.json", hash=hash),
            }


def get_commits(hash: str = "HEAD") -> list[str]:
    path = Path(config.CANON) / config.WORKING
    branch = Cache.canon.id
    commits, ret = git.run_git_command(path, 'log', '--oneline', hash,  '--', branch)
    branch_hash = Cache.canon.hash[0:7]
    return [line.split(" ")[0] for line in commits.splitlines()] + [branch_hash]


@publish_router.get("/changes/{hash}")
async def changes_by_hash(request: Request, hash: str):
    resp = EntryResponse(request, "publish/changes.html")
    commits = get_commits()
    commits.reverse()
    resp.update(
            title="Changes",
            diffs=get_diffs(hash=hash),
            commits=commits,
            hash=hash,
            )
    return resp.as_response()

@publish_router.get("/changes/")
async def changes(request: Request):
    resp = EntryResponse(request, "publish/changes.html")
    commits = get_commits()
    commits.reverse()
    hash = Cache.canon.hash[0:7]
    resp.update(
            title="Changes",
            diffs=get_diffs(hash=hash),
            commits=commits,
            hash=hash,
            )
    return resp.as_response()


def tree_tracker(you: str) -> list[str]:
    """ Get the number of commits in the working directory and the canonical repository """
    path = Path(config.CANON) / config.WORKING
    out, ret = git.run_git_command(path, 'rev-list', '--left-right', '--count', f'{config.WORKING}...{you}')
    if ret is False:
        return ["error", "error"]
    return out.split("\t")


@publish_router.get("/launch/")
async def launch(request: Request):
    resp = EntryResponse(request, "publish/launch.html")
    resp.update(
            title="Launch",
            site_map=Cache.site_map,
            tree_tracker=tree_tracker,
            )

    return resp.as_response()


@publish_router.get("/status/")
async def status(request: Request):
    resp = EntryResponse(request, "publish/status.html")
    resp.update( title="Status")
    return resp.as_response()


