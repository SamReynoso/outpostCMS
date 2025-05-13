from fastapi import Request

import config
from bin.run import app
from lib.response import PFResponse
from bin.routers.api import api_router 
from bin.routers.metadata import metadata_router
from bin.routers.projects import project_router
from lib.loadsite import load_zip_map

@app.get("/")
async def home(request: Request):
    resp = PFResponse(request, "home.html")
    resp.update(title="Content Management System")
    return resp()

@app.get("/console/")
async def console(request: Request):
    resp = PFResponse(request, "console.html")
    resp.update(
        title="Content Console",
        zip_map=load_zip_map(),
    )
    return resp()


@app.get("/archive/")
async def archive(request: Request):
    resp = PFResponse(request, "archive.html")
    resp.update(title="Archive")
    return resp()


@app.get("/gallery/")
async def gallery(request: Request):
    resp = PFResponse(request, "about.html")
    resp.update( title="Gallery",)
    return resp()


app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(metadata_router, prefix="/metadata", tags=["metadata"])
app.include_router(project_router, prefix="/projects", tags=["projects"])

if __name__ == "__main__":
    print("Starting the development server on port", config.DEV_PORT)
    import uvicorn
    uvicorn.run(
        "bin.dev:app",
        port=config.DEV_PORT,
        log_level="info",
        reload=True,
    )
