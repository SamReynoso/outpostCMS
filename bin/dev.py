from fastapi import Request

import config
from bin.run import app
from lib.locached import Cache
from lib.response import PFResponse

from bin.routers.api import api_router 
from bin.routers.meta import meta_router
from bin.routers.publish import publish_router


@app.get("/")
async def home(request: Request):
    resp = PFResponse(request, "quick-start.html")
    resp.update(title="Outpost CMS")
    return resp()


@app.get("/endpoints/")
async def endpoints(request: Request):
    resp = PFResponse(request, "endpoints.html")
    resp.update(title="API Endpoints")
    return resp()


app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(meta_router, prefix="/publish", tags=["publish"])
app.include_router(publish_router, prefix="/metadata", tags=["metadata"])


if __name__ == "__main__":
    print("Starting the development server on port", config.DEV_PORT)
    import uvicorn
    uvicorn.run(
        "bin.dev:app",
        port=config.DEV_PORT,
        log_level="info",
        reload=True,
    )
