from fastapi import APIRouter, Form
from lib.create import create_project as create_project_structure
from fastapi.responses import RedirectResponse



project_router = APIRouter()


@api_router.post("/edit-metadata/")
async def create_project(
        group: str = Form(...), 
        project_name: str = Form(...),
        canonical: str = Form(...)):
    create_project_structure(group, project_name, canonical)
    return RedirectResponse(url="/", status_code=303)


@app.get("/delete/{group}/{project_name}/")
async def delete(request: Request, group: str, project_name: str):
    resp = PFResponse(request, "about.html")
    resp.update(
            title="Delete Project",
            group=group,
            project_name=project_name
            )
    return resp()
