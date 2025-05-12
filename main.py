import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")
BASE_TEMPLATE_DIR = Path("templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    meta_path = BASE_TEMPLATE_DIR / "meta.json"
    if not meta_path.exists():
        raise HTTPException(status_code=404, detail="Index page not found")

    with open(meta_path) as f:
        meta = json.load(f)

    articles_meta_path = BASE_TEMPLATE_DIR / "articles.json"
    if not articles_meta_path.exists():
        raise HTTPException(status_code=404, detail="Articles meta not found")

    with open(articles_meta_path) as f:
        articles_meta = json.load(f)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "meta": meta,
            "articles": articles_meta,
        },
    )

@app.get("/build-log/{article_name}/", response_class=HTMLResponse)
async def build_log_page(request: Request, article_name: str):
    article_fragment = f"build-log/{article_name}/index.html"
    full_path = BASE_TEMPLATE_DIR / article_fragment
    meta_path = BASE_TEMPLATE_DIR / "build-log" / article_name / "meta.json"

    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Build log not found")

    with open(meta_path) as f:
        meta = json.load(f)

    return templates.TemplateResponse(
        "article.html",
        {
            "request": request,
            "meta": meta,
            "dynamic_article": article_fragment,
        },
    )

@app.get("/{article_name}/", response_class=HTMLResponse)
async def article_page(request: Request, article_name: str):
    article_fragment = f"{article_name}/index.html"
    full_path =  BASE_TEMPLATE_DIR / article_fragment
    meta_path = BASE_TEMPLATE_DIR / article_name / "meta.json"

    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Article not found")

    with open(meta_path) as f:
        meta = json.load(f)

    return templates.TemplateResponse(
        "article.html",
        {
            "request": request,
            "meta": meta,
            "dynamic_article": article_fragment,
        },
    )
