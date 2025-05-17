# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

from fastapi import APIRouter, Form, File, UploadFile
from fastapi.responses import RedirectResponse

import config
from lib.create import create_project


api_router = APIRouter()


@api_router.post("/new/")
async def new_project(
        group: str = Form(...), 
        project_name: str = Form(...),
        canonical: str = Form(...)
        ):
    path = Path(config.CANON) / config.WORKING
    create_project(path, group, project_name, canonical)
    return RedirectResponse(url=f"/upload/", status_code=303)


@api_router.post("/upload/")
async def upload_file(index_file: UploadFile = File(...)):
    file_path = "index.html"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(index_file.file, buffer)
    return RedirectResponse(url=f"/preview/", status_code=303)


@api_router.post("/canonical/")
async def update_canonical(
        group: str = Form(...), 
        project_name: str = Form(...),
        canonical: str = Form(...)
        ):
    return RedirectResponse(url=f"metadata/basic/", status_code=303)
