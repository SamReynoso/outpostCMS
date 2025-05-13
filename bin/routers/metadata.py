from fastapi import APIRouter, Request
from lib.response import PFResponse


metadata_router = APIRouter()


@metadata_router.get("/basic/{group}/{project_name}/")
async def basic_meta(request: Request, group: str, project_name: str):
    resp = PFResponse(request, "basic-metadata.html")
    resp.update(
            title="Basic Metadata",
            group=group,
            project_name=project_name
            )
    return resp()
