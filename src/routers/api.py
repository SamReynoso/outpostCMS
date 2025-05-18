import shutil
from pathlib import Path

from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import RedirectResponse

from outpost_d import config
from lib.locached import Cache




api_router = APIRouter()

def from_form(form, model):
    values = {}
    for field in model.__fields__:
        if field in form:
            values[field] = form[field]
        else:
            values[field] = None
    return model(**values)

class Canonical(BaseModel):
    group: str
    project: str
    canonical: str

@api_router.post("/new/")
async def new_project(request: Request):
    form = await request.form()
    canonical = from_form(form, Canonical)
    print(canonical)
    return RedirectResponse(url=f"/metadata/upload/", status_code=303)


@api_router.post("/upload/")
async def upload_file(index_file: UploadFile = File(...)):
    entry = Cache.project
    file_path = Path(config.WORKING) / entry.id / "index.html"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(index_file.file, buffer)
    return RedirectResponse(url=f"/metadata/basic/", status_code=303)


@api_router.post("/canonical/")
async def update_canonical():
    return RedirectResponse(url=f"/metadata/basic/", status_code=303)


@api_router.post("/basic/")
async def update_basic():
    return RedirectResponse(url=f"/metadata/social/", status_code=303)


@api_router.post("/social/")
async def update_social():
    return RedirectResponse(url=f"/metadata/advanced/", status_code=303)


@api_router.post("/advanced/")
async def update_advanced():
    return RedirectResponse(url=f"/publish/workbook/", status_code=303)


