import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from outpost_d import config


app = FastAPI()
app.mount("/static", StaticFiles(directory=config.STATIC_DIR))


PLACEHOLDER_KEY= "group-name/article-name"
PLACEHOLDER_FRAGMENT = "<h1>Sample Title</h1><p>Sample content</p>"

PLACEHOLDER_ENTRY = {
            "canonical": "https://example.com/article/group-name/article-name",
            "group": "group-name",
            "project": "project-name",
            "meta": {
                "basic": {
                    "title": "Sample Title",
                    "description": "Sample description",
                    "author": "John Smith",
                    "date": "2023-10-01",
                    "last_update": "2023-10-01"
                    },
                }

            }

@app.get("/articles/{path: path}/", response_class=JSONResponse)
async def articles_entry(path:str):
    """ Returns article fragment and basic metadata as JSON """
    del path
    content = {
            "entry": PLACEHOLDER_ENTRY,
            "fragment": PLACEHOLDER_FRAGMENT,
            }
    return JSONResponse(content=content)


@app.get("/articles/{group}/", response_class=JSONResponse)
async def articles_group(group:str):
    """ Returns article fragment and basic metadata as JSON """
    assert group == PLACEHOLDER_ENTRY["group"]
    content = [
            {
                "entry": PLACEHOLDER_ENTRY,
                "fragment": PLACEHOLDER_FRAGMENT,
                },
            ]
    return JSONResponse(content=content)

@app.get("/articles/", response_class=JSONResponse)
async def articles():
    """ Returns article fragment and basic metadata as JSON """
    content = [
            {
                "entry": PLACEHOLDER_ENTRY,
                "fragment": PLACEHOLDER_FRAGMENT,
                },
            ]
    return JSONResponse(content=content)


@app.get("/projects/{group}/", response_class=JSONResponse)
async def projects_group(path:str, group:str):
    """ Returns project metadata as JSON """
    assert group == PLACEHOLDER_ENTRY["group"]
    content = [
            {
                "group": PLACEHOLDER_ENTRY["group"],
                "project": PLACEHOLDER_ENTRY["project"],
                }
            ]
    return JSONResponse(content=content)

@app.get("/projects/", response_class=JSONResponse)
async def projects():
    """ Returns project metadata as JSON """
    content = [
            {
                "group": PLACEHOLDER_ENTRY["group"],
                "project": PLACEHOLDER_ENTRY["project"],
                }
            ]
    return JSONResponse(content=content)


@app.get("/info/", response_class=JSONResponse)
async def info():
    """ Returns full archive metadata as JSON """
    content = {
            PLACEHOLDER_KEY: PLACEHOLDER_ENTRY,
            }
    return JSONResponse(content=content)


@app.get("/info/{group}", response_class=JSONResponse)
async def info_group(group: str):
    """ Returns group metadata as JSON """
    assert group == PLACEHOLDER_ENTRY["group"]
    content = {
            PLACEHOLDER_KEY: PLACEHOLDER_ENTRY,
            }
    return JSONResponse(content=content)


@app.get("/info/{group}/{path: path}/", response_class=JSONResponse)
async def info_entry(group: str, path:str):
    """ Returns group entry metadata as JSON """
    assert group == PLACEHOLDER_ENTRY["group"]
    assert path == PLACEHOLDER_ENTRY["project"]
    content = {
            "entry": PLACEHOLDER_ENTRY,
            }
    return JSONResponse(content=content)


@app.get("/groups/", response_class=JSONResponse)
async def groups():
    """ Returns all groups as JSON """
    content = [PLACEHOLDER_ENTRY["group"]]
    return JSONResponse(content=content)


@app.get("/robots/{path: path}/", response_class=Response)
async def robots_entry(path:str):
    """ Returns robots.txt entry as plain text """
    return Response(content=f"No data found for {path}.", media_type="application/json")


@app.get("/robots/group/", response_class=Response)
async def robots_group(path:str):
    """ Returns robots.txt group as plain text """
    return Response(content=f"No data found for {path}.", media_type="application/json")


@app.get("/robots/", response_class=Response)
async def robots(path:str):
    """ Returns robots.txt for the entire archive as plain text """
    return Response(content=f"No data found for {path}.", media_type="application/json")

@app.get("/head/basic/{path: path}/", response_class=Response)
async def head_basic(path:str):
    """ Returns basic metadata as plain text """
    return Response(content=f"No data found for {path}.", media_type="application/json")


@app.get("/head/social/{path: path}/", response_class=Response)
async def head_social(path:str):
    """ Returns social metadata as plain text """
    return Response(content=f"No data found for {path}.", media_type="application/json")


@app.get("/head/json-dl/{path: path}/", response_class=Response)
async def head_json_dl(path:str):
    """ Returns JSON download metadata as plain text """
    return Response(content=f"No data found for {path}.", media_type="application/json")


@app.get("/head/full/{path: path}/", response_class=Response)
async def head_full(path:str):
    """ Returns full metadata as plain text """
    return Response(content=f"No data found for {path}.", media_type="application/json")


if __name__ == "__main__":
    print("Starting the production server on port", config.PROD_PORT)
    import uvicorn
    uvicorn.run(
        "bin.run:app",
        port=config.PROD_PORT,
        log_level="info",
        reload=False,
    )
