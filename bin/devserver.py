from bin.server import app
from canonical import config
from fastapi import FastAPI

from fastapi import Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

from lib.loadsite import load_everything

templates = Jinja2Templates(directory="templates")


ALL_ARTICLES = []
CANONICAL_INDEX = {}


def update_cache():
    """Update the cache by loading all articles."""
    global ALL_ARTICLES, CANONICAL_INDEX
    ALL_ARTICLES = load_everything()
    CANONICAL_INDEX = {entry["canonical"]: entry for entry in ALL_ARTICLES}


@app.get("/")
async def nav(request: Request):
    update_cache()
    return templates.TemplateResponse(
        "nav.html",
        {
            "request": request,
            "articles": ALL_ARTICLES,
        },
    )


@app.get("/edit/meta/{canonical_path:path}/")
async def meta(request: Request, canonical_path: str):
    article = CANONICAL_INDEX.get(canonical_path)
    if not article:
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse(
        "meta.html",
        {
            "request": request,
            "meta": article,
        },
    )



if __name__ == "__main__":
    print("Starting the editor on port", config.EDITOR_PORT)
    print("the editor is open")
    import uvicorn
    uvicorn.run(
        "bin.editor:app",
        port=config.EDITOR_PORT,
        log_level="info",
        reload=True,
    )

