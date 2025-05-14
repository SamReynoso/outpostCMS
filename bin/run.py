import json
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from lib.loadsite import load_fragment, load_zip_map
import config


app = FastAPI()
app.mount("/" + config.STATIC_DIR, StaticFiles(directory="static"), name="static")


@app.get("/article/{canonical:path}/", response_class=JSONResponse)
async def article_page(_, canonical:str):
    pass


@app.get("/info/", response_class=JSONResponse)
async def info_page():
    data = load_zip_map()
    pretty_data = json.dumps(data, indent=4, ensure_ascii=False)
    return Response(content=pretty_data, media_type="application/json")


if __name__ == "__main__":
    print("Starting the production server on port", config.PROD_PORT)
    import uvicorn
    uvicorn.run(
        "bin.run:app",
        port=config.PROD_PORT,
        log_level="info",
        reload=False,
    )
