from datetime import datetime
import shutil
from pathlib import Path

from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import RedirectResponse

from outpost_d import config
from lib.locached import Cache
from src.data import CacheControl as cc
from src.models import Canonical, Basic, Social, Advanced
from lib import git, fsutils


api_router = APIRouter()


@api_router.post("/new/")
async def new_project(request: Request):
    form = dict(await request.form())
    canonical = Canonical(hash=None, public=False, **form)
    working_dir = Path(config.CANON) / config.WORKING
    output, ret = git.commit(working_dir, f"{canonical.id}: Created")
    if ret is False:
        print(f"[Error  ] {output}")
    git.add(working_dir)
    _, ret = git.merge(working_dir, config.PUBLISH)
    _, ret = git.checkout(working_dir, config.PUBLISH)
    hash, ret = git.branch(working_dir, canonical.id)
    canonical.hash = hash
    cc.create_project(canonical)
    fsutils.write(working_dir / canonical.id / "index.html", "<section></section>")
    return RedirectResponse(url=f"/metadata/upload/", status_code=303)


@api_router.post("/upload/")
async def upload_file(index_file: UploadFile = File(...)):
    canon = Cache.canon
    file_path = Path(config.CANON) / config.WORKING / canon.id / "index.html"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(index_file.file, buffer )
    return RedirectResponse(url=f"/metadata/basic/", status_code=303)


@api_router.post("/canonical/")
async def update_canonical(request: Request):
    form = dict(await request.form())
    canon = Cache.canon
    cc.Update.canonical(Canonical(hash=canon.hash, public=canon.public, **form))
    return RedirectResponse(url=f"/metadata/basic/", status_code=303)


@api_router.post("/basic/")
async def update_basic(request: Request):
    form = dict(await request.form())
    basic = Basic(**form)
    cc.Update.basic(basic)
    return RedirectResponse(url=f"/metadata/social/", status_code=303)


@api_router.post("/social/")
async def update_social(request: Request):
    form = dict(await request.form())
    cc.Update.social(Social(**form))
    return RedirectResponse(url=f"/metadata/advanced/", status_code=303)


@api_router.post("/advanced/")
async def update_advanced(request: Request):
    form = dict(await request.form())
    cc.Update.advanced(Advanced(**form))
    return RedirectResponse(url=f"/publish/workbook/", status_code=303)


@api_router.get("/commit/")
async def commit():
    path = Path(config.CANON) / config.WORKING / Cache.canon.id
    git.add(path)
    git.commit(path, f"{Cache.canon.id}: Updated")
    return RedirectResponse(url=f"/publish/workbook/", status_code=303)


@api_router.get("/checkout/{group}/{project}")
async def checkout(group: str, project: str):
    path = Path(config.CANON) / config.WORKING
    branch = f"{group}/{project}"
    git.add(path)
    git.commit(path, f"Switching branches: {Cache.canon.id} -> {branch}")
    git.checkout(path, branch)
    git.merge(path, config.PUBLISH, "Merging current published changes")
    return RedirectResponse(url=f"/publish/workbook/", status_code=303)


@api_router.get("/toggle/{group}/{project}")
async def toggle(group: str, project: str):
    canon = Cache.site_map.get(f"{group}/{project}", None)
    if canon is None:
        return RedirectResponse(url=f"/publish/launch/", status_code=303)
    canon.public = not canon.public
    cc.Update.canonical(canon)
    return RedirectResponse(url=f"/publish/launch#{group}_{project}", status_code=303)


@api_router.get("/launch/{group}/{project}")
async def launch(group: str, project: str):
    project_id = f"{group}/{project}"
    path = Path(config.CANON) / config.PUBLISH
    working_dir = Path(config.CANON) / config.WORKING / project_id
    git.add(working_dir)
    git.commit(working_dir, f"{project_id}: Saving changes")
    git.merge(working_dir, config.PUBLISH, message="Merging any new published changes")
    git.merge(path, project_id, f"{project_id}: Publishing changes to")
    return RedirectResponse(url=f"/publish/launch/", status_code=303)




