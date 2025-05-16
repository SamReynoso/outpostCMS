
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

import config
from lib.locached import Cache
from lib import git
from lib.response import PFResponse
from typing import Optional
from fastapi import Request, Query


git_router = APIRouter()



@git_router.get("/")
async def publish(request: Request):
    site_map = Cache.get_site_map()
    for entry in site_map:
        changes = git.change_log(config.WORKING, entry['group'], entry['project_name'])
        entry['changes'] = changes
    resp = PFResponse(request, "publish/publish.html")
    resp.update(
            title="Publishing Pipeline",
            site_map=site_map,
            )
    return resp()
