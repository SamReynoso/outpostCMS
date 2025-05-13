from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from lib.loadsite import Cache, load_fragment
import config


app = FastAPI()
app.mount("/" + config.STATIC_DIR, StaticFiles(directory="static"), name="static")
app.mount("/" + config.ASSETS_DIR, StaticFiles(directory="assets"), name="assets")


@app.get("/article/{canonical:path}/", response_class=JSONResponse)
async def article_page(_, canonical:str):
    metadata= Cache.get(canonical)
    fragment = load_fragment(metadata)
    return JSONResponse(content={"meta": metadata, "fragment": fragment})


@app.get("/info/", response_class=JSONResponse)
async def info_page(_):
    Cache.update_on_interval()
    return JSONResponse(content={"site_map": Cache.site_map()})


if __name__ == "__main__":
    print("Starting the production server on port", config.PROD_PORT)
    import uvicorn
    uvicorn.run(
        "bin.run:app",
        port=config.PROD_PORT,
        log_level="info",
        reload=False,
    )
