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


@app.get("/")
async def nav(request: Request):
    articles = load_everything()
    return templates.TemplateResponse(
        "nav.html",
        {
            "request": request,
            "articles": articles,
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

