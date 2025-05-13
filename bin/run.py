import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn

from lib.loadsite import load_and_validate_site_data
from canonical import config


SITE_META = []
CANONICAL_INDEX = {}
LAST_LOAD = 0

def check_cache():
    global LAST_LOAD, SITE_META, CANONICAL_INDEX
    uptime = time.time() - LAST_LOAD
    if uptime > 60 * 60:
        print("[INFO] Reloading site data")
        SITE_META = load_and_validate_site_data()
        CANONICAL_INDEX = {entry["canonical"]: entry for entry in SITE_META}
        LAST_LOAD = time.time()



def load_fragment(content_dir: str) -> str:
    content_path = Path(content_dir)
    fragment_path = content_path / "index.html"
    if not fragment_path.is_file():
        print(f"[ERROR] File for fragment not found: {fragment_path}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    try:
        with open(fragment_path) as f:
            return f.read()
    except IOError:
        raise HTTPException(status_code=500, detail="Internal Server Error")


TEMPLATES = Jinja2Templates(directory=config.TEMPLATES_DIR)
app = FastAPI()
app.mount("/" + config.STATIC_DIR, StaticFiles(directory="static"), name="static")
app.mount("/" + config.ASSETS_DIR, StaticFiles(directory="assets"), name="assets")


@app.get("/archive/", response_class=HTMLResponse)
async def index(request: Request):
    check_cache()
    return TEMPLATES.TemplateResponse(
        "archive.html",
        {
            "request": request,
            "articles": SITE_META,
        },
    )


@app.get("/archive/{article_path:path}/", response_class=HTMLResponse)
async def article_page(request: Request, article_path: str):
    entry = CANONICAL_INDEX.get(article_path)
    if not entry:
        print(f"[ERROR] Article not found: {article_path}")
        raise HTTPException(status_code=404, detail="Article not found")
    fragment = load_fragment(entry["path"])
    return TEMPLATES.TemplateResponse(
        "page.html",
        {
            "request": request,
            "article_fragment": fragment,
            "meta": entry,
        },
    )


if __name__ == "__main__":
    print("Starting the production server on port", config.PROD_PORT)
    import uvicorn
    uvicorn.run(
        "bin.run:app",
        port=config.PROD_PORT,
        log_level="info",
        reload=False,
    )

