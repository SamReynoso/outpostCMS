from fastapi import Request, APIRouter

from lib.response import PFResponse



project_router = APIRouter()


@project_router.get("/")
async def list_project(request: Request):
    resp = PFResponse(request, "about.html")
    resp.update(title="Projects")
    return resp()


@project_router.get("/{group}/{project_name}/preview/")
async def preview_project(request: Request, group: str, project_name: str):
    resp = PFResponse(request, "preview.html")
    resp.update(
            title="Preview",
            group=group,
            project_name=project_name
            )
    return resp()


@project_router.get("/{group}/{project_name}/")
async def project(request: Request, group: str, project_name: str):
    resp = PFResponse(request, "about.html")
    resp.update(
        title="Project",
        group=group,
        project_name=project_name
    )
    return resp()
