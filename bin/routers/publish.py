import json
from pathlib import Path

from fastapi import APIRouter


import config
from lib.locached import Cache
from lib import git
from lib.response import PFResponse
from fastapi import Request

        
def get_working_dir():
    return Path(config.CANON) / config.WORKING


publish_router = APIRouter()


@publish_router.get("/")
async def publish(request: Request):
    site_map = Cache.all()
    for entry in site_map:
        changes = git.change_log(get_working_dir(), entry['group'], entry['project_name'])
        entry['changes'] = changes
    resp = PFResponse(request, "publish/publish.html")
    resp.update(
            title="Publishing",
            site_map=site_map,
            )
    return resp()


@publish_router.get("/preview/")
async def preview(request: Request):
    entry = Cache.get_project("outpost", "preview")
    resp = PFResponse(request, "preview.html")
    resp.update(
            title="Preview " + entry.get("title", "unknown"),
            group=group,
            project_name=project_name,
            entry=entry,
            article_fragment=load_fragment(group, project_name)
            )
    return resp()



@publish_router.get("/workbook/")
async def workbook(request: Request):
    working_dir = get_working_dir()
    group, project_name = git.current_branch(working_dir).split("/")
    entry = Cache.get_project(group, project_name)
    resp = PFResponse(request, "publish/workbook.html")
    resp.update(
            title="Workbook",
            entry=entry,
            changes=git.change_log(working_dir, group, project_name),
            index_diff=git.diff_index(working_dir, group, project_name),
            meta_diff=git.diff_meta(working_dir, group, project_name),
            )
    return resp()


@publish_router.get("/changes/")
async def changes(request: Request):
    working_dir = get_working_dir()
    entry = Cache.get_project(group, project_name)
    resp = PFResponse(request, "publish/diff.html")
    meta = git.diff_meta(working_dir, group, project_name)
    index = git.diff_index(working_dir, group, project_name)
    resp.update(
            title="Changes",
            entry=entry,
            status=git.status(working_dir, group, project_name),  
            changes=git.change_log(working_dir, group, project_name),
            index_diff=format_index_diff(index),
            meta_diff=format_meta_diff(meta),
            )
    return resp()


@publish_router.get("/submit/")
async def commit(request: Request, group: str, project_name: str):
    entry = Cache.get_project(group, project_name)
    resp = PFResponse(request, "publish/commit.html")
    resp.update(
            title="Changes",
            entry=entry,
            )
    return resp()


@publish_router.get("/launch/")
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


@publish_router.get("/status/")
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
