from pathlib import Path

from fastapi import APIRouter

import config
from lib.locached import Cache
from lib import git
from lib.response import PFResponse
from fastapi import Request


git_router = APIRouter()


def get_working_dir():
    return Path(config.CANON) / config.WORKING


@git_router.get("/")
async def workbook(request: Request):
    working_dir = get_working_dir()
    group, project_name = git.current_branch(working_dir).split("/")
    entry = Cache.get_project(group, project_name)
    resp = PFResponse(request, "publish/workbook.html")
    resp.update(
            title="Workbook",
            entry=entry,
            changes=git.change_log(working_dir, group, project_name),
            index_diff=git.index_diff(working_dir, group, project_name),
            meta_diff=git.meta_diff(working_dir, group, project_name),
            )
    return resp()


@git_router.get("/staging/")
async def staging(request: Request):
    site_map = Cache.get_site_map()
    for entry in site_map:
        changes = git.change_log(get_working_dir(), entry['group'], entry['project_name'])
        entry['changes'] = changes
    resp = PFResponse(request, "publish/staging.html")
    resp.update(
            title="Staging",
            site_map=site_map,
            )
    return resp()


@git_router.get("/launch/")
async def launch(request: Request):
    site_map = Cache.get_site_map()
    for entry in site_map:
        changes = git.change_log(get_working_dir(), entry['group'], entry['project_name'])
        entry['changes'] = changes
    resp = PFResponse(request, "publish/launch.html")
    resp.update(
            title="Launch",
            site_map=site_map,
            )
    return resp()


@git_router.get("/status/")
async def status(request: Request):
    site_map = Cache.get_site_map()
    for entry in site_map:
        changes = git.change_log(get_working_dir(), entry['group'], entry['project_name'])
        entry['changes'] = changes
    resp = PFResponse(request, "publish/status.html")
    resp.update(
            title="Status",
            site_map=site_map,
            )
    return resp()
