
from fastapi import APIRouter, Request

from outpost_d import config
from lib.locached import Cache
from lib.response import EntryResponse 



publish_router = APIRouter()


@publish_router.get("/")
async def index(request: Request):
    resp = EntryResponse(request, "publish/index.html")
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


@publish_router.get("/changes/")
async def changes(request: Request):
    resp = EntryResponse(request, "publish/changes.html")
    resp.update(
            title="Changes",
            changes="",
            index_diff="",
            meta_diff="",
            )
    return resp.as_response()


@publish_router.get("/submit/")
async def commit(request: Request):
    resp = EntryResponse(request, "publish/commit.html")
    resp.update( title="Changes")
    return resp.as_response()


@publish_router.get("/launch/")
async def launch(request: Request):
    resp = EntryResponse(request, "publish/launch.html")
    resp.update(title="Launch")
    return resp.as_response()


@publish_router.get("/status/")
async def status(request: Request):
    resp = EntryResponse(request, "publish/status.html")
    resp.update( title="Status")
    return resp.as_response()


