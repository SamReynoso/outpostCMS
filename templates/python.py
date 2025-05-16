import time
from dataclasses import dataclass, asdict
from typing import Dict

EDITOR_UNDER_CONSTRUCTION = """<html><head><title>Editor</title></head><body><h1>Editor</h1><p>Editor is not implemented
yet.</p></body></html>"""

PUBLISH_REPOSITORY_README = """
# Publish Repository
This README should help you understand the purpose of this repository. This repo is the target of the CMS API when
serving content in production mode. This repository is the canonical repository for the CMS API. Works in progress
should be done in the working directory. This worktree has a different branch for each project which can be merged
into main in the publish directory. The publish directory should always have main checked out.
"""

WORKING_REPOSITORY_README = """
# Working Worktree
The working directory holds all works in progress. The server does not access this directory when in production mode.
changes made through the browser interface should ensure that each project branch only contains changes related to the
corresponding project directory. With the main branch always being checked out in the publish branch you should feel
secure that none of your work will be served to the client until you are ready to publish and merge them into main.
"""

def new_site_map_entry(group: str, project_name: str, canonical: str):
    return {
        "group": group.strip(),
        "project_name": project_name.strip(),
        "canonical": canonical.strip(),
        "public": False,
    }


def new_metadata():
    date = time.strftime("%Y-%m-%d")
    return {
            "title": "Untitled",
            "description": "",
            "keywords": "",
            "author": "",
            "date": date,
            "last_updated": date,
            }


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


NEW_PROJECT_DIS = '''
<h2>Project Structure</h2>
The content management system uses the information entered in this form the maintain a mapping between canonical URLs
and your project. The information is used to generate accurate SEO metatags and search engine submissions. The 
information is also used to generate sitemap.xml and robots.txt files for your server.
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


FORMS = {
    "new": MetaForm(
        target="metadata/canonical.html",
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
        target="projects/upload.html",
        title="Upload Project",
        form_action="this must be filled in dynamically",
        form_header="Upload Project",
        form_description=INDEX_HTML_DIS,
    ),
}

