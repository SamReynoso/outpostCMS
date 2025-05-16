
from fastapi import Request, APIRouter
from fastapi.exceptions import HTTPException

from lib.locached import Cache, load_fragment
from lib.response import PFResponse, MetadataResponse
from templates.python import FORMS


def entry_or_404(group: str, project_name: str):
    entry = Cache.get_project(group, project_name)
    if entry is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return entry


def return_form_response(request: Request, name: str, group: str, project_name: str):
    entry = entry_or_404(group, project_name)
    form = FORMS.get(name)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    resp = MetadataResponse(request, form.target)
    resp.update(entry=entry, **form.data)
    return resp()


project_router = APIRouter()


@project_router.get("/new/")
async def new_project(request: Request):
    resp = PFResponse(request, "metadata/canonical.html")
    resp.update(entry={}, **FORMS['new'].data)
    return resp()


@project_router.get("/{group}/{project_name}/canonical/")
async def meta_canonical(request: Request, group: str, project_name: str):
    return return_form_response(request, "canonical", group, project_name)


@project_router.get("/{group}/{project_name}/basic/")
async def meta_basic(request: Request, group: str, project_name: str):
    return return_form_response(request, "basic", group, project_name)


@project_router.get("/{group}/{project_name}/social/")
async def meta_social(request: Request, group: str, project_name: str):
    return return_form_response(request, "social", group, project_name)


@project_router.get("/{group}/{project_name}/advanced/")
async def meta_advanced(request: Request, group: str, project_name: str):
    return return_form_response(request, "advanced", group, project_name)


@project_router.get("/{group}/{project_name}/upload/")
async def index_html_upload(request: Request, group: str, project_name: str):
    resp = PFResponse(request, "projects/upload.html")
    resp.update(
            entry=entry_or_404(group, project_name),
            **FORMS['upload'].data
            )
    # This line a a hack. Form action from FORMS is being overwritten to be dynamic.
    # I don't feel like adding hidden fields to the form.
    # Or changing the post logic in the api router.
    resp.update(form_action=f"/api/projects/upload/{group}/{project_name}/")
    return resp()


'''




The form routs stop here and the next function is a preview of the project
'''
@project_router.get("/{group}/{project_name}/preview/")
async def preview_project(request: Request, group: str, project_name: str):
    entry = entry_or_404(group, project_name)
    print(entry)
    resp = PFResponse(request, "preview.html")
    resp.update(
            title="Preview " + entry.get("title", "unknown"),
            group=group,
            project_name=project_name,
            entry=entry,
            article_fragment=load_fragment(group, project_name)
            )
    return resp()


