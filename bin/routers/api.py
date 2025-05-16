# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

from fastapi import APIRouter, Form, File, UploadFile
from lib.create import create_project as create_project_structure
from fastapi.responses import RedirectResponse

import config


api_router = APIRouter()



@api_router.post("/projects/new/")
async def create_project(
        group: str = Form(...), 
        project_name: str = Form(...),
        canonical: str = Form(...)):
    create_project_structure(group, project_name, canonical)
    return RedirectResponse(url=f"/projects/{ group }/{ project_name }/upload/", status_code=303)


@api_router.post("/projects/upload/{group}/{project_name}/")
async def upload_file(
        group: str,
        project_name: str,
        index_file: UploadFile = File(...)
        ):
    upload_dir = Path(config.WORKING) / group / project_name
    if not upload_dir.exists():
        return {"error": "Project directory does not exist."}

    file_path = upload_dir / "index.html"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(index_file.file, buffer)

    return RedirectResponse(url=f"/projects/{ group }/{ project_name }/preview/", status_code=303)

