from fastapi import Request, APIRouter, HTTPException
from lib.loadsite import Cache, load_fragment
from lib.response import PFResponse

from lib.loadsite import load_fragment, load_meta



project_router = APIRouter()


@project_router.get("/")
async def list_project(request: Request):
    resp = PFResponse(request, "about.html")
    resp.update(title="Projects")
    return resp()

@project_router.get("/new/")
async def new_project(request: Request):
    resp = PFResponse(request, "metadata/basic.html")
    
    resp.update(
        title="New Project",
        form_action="/api/projects/new/",
        form_header="Create a new project",
        form_description='''
<h2>Project Structure</h2>
The content management system uses the information entered in this form the maintain
a mapping between canonical URLs and your project. The information is used to generate
accurate SEO metatags and search engine submissions. The information is also used to
generate the sitemap.xml file.
''',
        meta={},
        )
    return resp()


@project_router.get("/{group}/{project_name}/canonical/")
async def project_canonical(request: Request, group: str, project_name: str):
    resp = PFResponse(request, "metadata/basic.html")
    entry=Cache.get_project(group, project_name)
    if entry is None:
        raise HTTPException(status_code=404, detail="Project not found")

    resp.update(
        title="Update Project",
        form_action="/api/projects/update/",
        form_header="Update: " + entry["title"],
        form_description='''
<strong>Note:</strong> Changing the group or project name will not change canonical URL of the project. But will effect
the the API endpoint for the project that returns the article fragment.
''',
        meta=entry,
        )
    return resp()
@project_router.get("/{group}/{project_name}/info/")
async def project_info(request: Request, group: str, project_name: str):
    resp = PFResponse(request, "projects/info.html")
    resp.update(
            title="Project Info",
            entry=Cache.get_project(group, project_name),
            )
    return resp()



@project_router.get("/{group}/{project_name}/preview/")
async def preview_project(request: Request, group: str, project_name: str):
    resp = PFResponse(request, "preview.html")
    meta = load_meta(group, project_name)
    
    resp.update(
            title="Preview " + meta.get("title", "unknown"),
            group=group,
            project_name=project_name,
            article_fragment=load_fragment(group, project_name),
            meta=meta,
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
