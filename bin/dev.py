from fastapi import Request

from outpost_d import config
from bin.run import app
from lib.response import EntryResponse

from src.routers.api import api_router 
from src.routers.meta import meta_router
from src.routers.publish import publish_router


@app.get("/")
async def home(request: Request):
    resp = EntryResponse(request, "quick-start.html")
    resp.update(title="Outpost CMS")
    return resp.as_response()


@app.get("/endpoints/")
async def endpoints(request: Request):
    resp = EntryResponse(request, "endpoints.html")
    resp.update(title="API Endpoints")
    return resp.as_response()


app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(publish_router, prefix="/publish", tags=["publish"])
app.include_router(meta_router, prefix="/metadata", tags=["metadata"])


if __name__ == "__main__":
    print("Starting the development server on port", config.DEV_PORT)
    import uvicorn
    uvicorn.run(
        "bin.dev:app",
        port=config.DEV_PORT,
        log_level="info",
        reload=True,
    )
