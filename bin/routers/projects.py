from dataclasses import dataclass, asdict
from typing import Dict

from fastapi import Request, APIRouter
from fastapi.exceptions import HTTPException

from lib.loadsite import Cache, load_fragment
from lib.response import PFResponse, MetadataResponse
from lib.loadsite import load_fragment


def entry_or_404(group: str, project_name: str):
    entry = Cache.get_project(group, project_name)
    if entry is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return entry


NEW_PROJECT_DIS = '''
<h2>Project Structure</h2>
The content management system uses the information entered in this form the maintain a mapping between canonical URLs
and your project. The information is used to generate accurate SEO metatags and search engine submissions. The 
information is also used to generate the sitemap.xml file.
'''

CANONICAL_DIS = '''
<strong>Note:</strong> Changing the group or project name will not change canonical URL of the project. But will effect
the the API endpoint for the project that returns the article fragment.
'''

BASIC_DIS = '''
<strong>Note:</strong> Changing the group or project name will not change canonical URL of the project. But will effect
the the API endpoint for the project that returns the article fragment.
'''

SOCIAL_DIS = '''
<strong>Rich Preview:</strong> This is the information that will be used to generate the rich preview
by search social media sites. 
'''


ADVANCED_DIS = '''
<h2>Enhance Your Project’s Visibility</h2>

<p>
    Filling out this form helps generate rich previews and structured data for your project. These details power link
    previews on social media (like Facebook, Twitter, and LinkedIn) and improve how your project appears in search
    engines like Google.
</p>

<p>
<strong>Why it matters:</strong>
<ul>
    <li>Makes your project stand out in shared links</li>
    <li>Improves SEO and search result quality</li>
    <li>Helps users understand what your project does at a glance</li>
    <li>Encourages engagement and clicks</li>
<p>
    If you skip this step, your project may show up as a blank or generic link. Fill it out once, and your content looks
    polished everywhere it appears.
</p>
'''

INDEX_HTML_DIS = '''
<h2>Upload Your Project</h2>
<p>
    This is the information that will be used to generate the rich preview by search social media sites.
</p>
'''

@dataclass
class MetaForm:
    target: str
    title: str
    form_action: str
    form_header: str
    form_description: str

    @property
    def data(self) -> Dict[str, str]:
        if not self.title:
            raise ValueError("Form title not set")
        if not self.target:
            raise ValueError("Form target not set")
        if not self.form_action:
            raise ValueError("form_action not set")
        return asdict(self)


FORMS = {
    "new": MetaForm(
        target="metadata/cononical.html",
        title="New Project",
        form_action="/api/projects/new/",
        form_header="Create a new project",
        form_description=NEW_PROJECT_DIS,
    ),
    "canonical": MetaForm(
        target="metadata/canonical.html",
        title="Update Canonical",
        form_action="/api/canonical/update/",
        form_header="Update Project",
        form_description=CANONICAL_DIS,
    ),

    "basic": MetaForm(
        target="metadata/basic.html",
        title="Update Project",
        form_action="/api/basic/update/",
        form_header="Update Project",
        form_description=BASIC_DIS,
    ),

    "social": MetaForm(
        target="metadata/social.html",
        title="Social Metadata",
        form_action="/api/social/update/",
        form_header="Social Metadata",
        form_description=SOCIAL_DIS,
    ),

    "advanced": MetaForm(
        target="metadata/advanced.html",
        title="Advanced Metadata",
        form_action="/api/advanced/update/",
        form_header="Advanced Metadata",
        form_description=ADVANCED_DIS,
    ),

    "upload": MetaForm(
        target="metadata/index.html",
        title="Upload Project",
        form_action="/api/projects/upload/",
        form_header="Upload Project",
        form_description=INDEX_HTML_DIS,
    ),
}


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
    resp = MetadataResponse(request, "metadata/canonical.html")
    resp.update(**FORMS['new'].data)
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
    return return_form_response(request, "upload", group, project_name)


'''

The form routs stop here and the next function is a preview of the project

'''
@project_router.get("/{group}/{project_name}/preview/")
async def preview_project(request: Request, group: str, project_name: str):
    entry = entry_or_404(group, project_name)
    resp = PFResponse(request, "metadata/preview.html")
    resp.update( title="Preview " + entry.get("title", "unknown"), group=group, project_name=project_name, entry=entry, article_fragment=load_fragment(group, project_name),)
    return resp()
