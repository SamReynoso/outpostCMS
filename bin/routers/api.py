from fastapi import APIRouter, Form
from lib.create import create_project as create_project_structure
from fastapi.responses import RedirectResponse



api_router = APIRouter()



@api_router.post("/projects/new/")
async def create_project(
        group: str = Form(...), 
        project_name: str = Form(...),
        canonical: str = Form(...)):
    print('''








          this is working?





          ''')
    create_project_structure(group, project_name, canonical)
    return RedirectResponse(url="/", status_code=303)
