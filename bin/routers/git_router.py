import json
from pathlib import Path

from fastapi import APIRouter


import config
from lib.locached import Cache
from lib import git
from lib.response import PFResponse
from fastapi import Request


def format_meta_diff(diff):
    diff = diff.split("\n")
    html = "<dl>\n"
    start = False
    for i, line in enumerate(diff):
        if line.find("}") != -1:
            start = False
            continue
        line = line.strip()
        if start:
            cols = [val.strip() for val in line.split('"')]
            if cols[0] == "":
                html += f"<dt>{cols[1]}</dt>\n"
                html += f"<dd>{cols[3]}</dd>\n"
            if cols[0] == "-":
                html += f"<dt class='deleted'> - {cols[1]}</dt>\n"
                html += f"<dd class='deleted'> - {cols[3]}</dd>\n"
            if cols[0] == "+":
                html += f"<dt class='added'>+ {cols[1]}</dt>\n"
                html += f"<dd class='added'>+ {cols[3]}</dd>\n"


        if line.startswith("{"):
            start = True

    html += "</dl>\n"
    return html

def format_index_diff(diff):
    html = '<article class="diff">\n'
        
    lines = diff.split("\n")
    start = False
    for line in lines:
        if line.startswith('@'):
            start = True
            continue
        if not start:
            continue
        if line.startswith('+'):
            cleaned = line[1:].strip()
            if cleaned.startswith("<"):
                start = cleaned.find(">")
                assert start != -1
                cleaned = cleaned[:start] + ' class="add">' + cleaned[start + 1:]
            else:
                html += f'<span class="add">{cleaned}</span>\n'
            continue

        if line.startswith('-'):
            cleaned = line[1:].strip()
            if cleaned.startswith("<"):
                start = cleaned.find(">")
                assert start != -1, f"Start not found in {cleaned}"
                cleaned = cleaned[:start] + ' class="delete" ' + cleaned[start + 1:]
            else:
                html += f'<span class="delete">{cleaned}</span>\n'
            continue
        html += line + "\n"
        

    html += "</article>\n"
    return html
            
        
def get_working_dir():
    return Path(config.CANON) / config.WORKING


git_router = APIRouter()


@git_router.get("/")
async def staging(request: Request):
    site_map = Cache.all()
    for entry in site_map:
        changes = git.change_log(get_working_dir(), entry['group'], entry['project_name'])
        entry['changes'] = changes
    resp = PFResponse(request, "publish/staging.html")
    resp.update(
            title="Staging",
            site_map=site_map,
            )
    return resp()



@git_router.get("/workbook/")
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


@git_router.get("/changes/")
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


@git_router.get("/submit/")
async def commit(request: Request, group: str, project_name: str):
    entry = Cache.get_project(group, project_name)
    resp = PFResponse(request, "publish/commit.html")
    resp.update(
            title="Changes",
            entry=entry,
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
