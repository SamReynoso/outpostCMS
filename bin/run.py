import json
import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from outpost_d import config
from lib.wacached import Public
from src import tag_formatter


PLACEHOLDER_KEY= "group-name/article-name"
PLACEHOLDER_FRAGMENT = "<h1>Sample Title</h1><p>Sample content</p>"
PLACEHOLDER_ENTRY = {}


app = FastAPI()
app.mount("/static", StaticFiles(directory=config.STATIC_DIR))

@app.get("/info/", response_class=JSONResponse)
async def info():
    return Response(content=json.dumps(Public.site_metadata(), indent=2))

@app.get("/info/groups/", response_class=JSONResponse)
async def groups():
    return Response(content=json.dumps(Public.groups(), indent=4))


@app.get("/info/projects/", response_class=JSONResponse)
async def projects():
    return Response(content=json.dumps(Public.projects(), indent=4))

@app.get("/info/{group}", response_class=JSONResponse)
async def info_group(group: str):
    return JSONResponse(content=Public.group_metadata(group))

@app.get("/info/{group}/{project}/", response_class=JSONResponse)
async def info_entry(group: str, project:str):
    print(f"[DEBUG] route: info_entry({group}, {project})")
    return JSONResponse(content=Public.metadata(group, project))

@app.get("/articles/{group}/{project}/", response_class=JSONResponse)
async def articles_entry(group:str, project:str):
    return Response(content=Public.fragment(group, project))

@app.get("/head/{group}/{project}/", response_class=Response)
async def head_full(group:str, project:str):
    canon = Public.canon(group, project)
    metadata = Public.metadata(group, project)
    return Response(content=tag_formatter.head_full(canon, metadata))








# @app.get("/articles/{group}/", response_class=JSONResponse)
# async def articles_group(group:str):
#     fragments = Public.group_fragments(group)
#     return JSONResponse(content=fragments)
# 
# @app.get("/articles/", response_class=JSONResponse)
# async def articles():
#     return JSONResponse(content=json.dumps(Public.site_fragments(), indent=4))
# 
# 
# 
# 
# 
# 
# 
# # @app.get("/groups/", response_class=JSONResponse)
# # async def groups():
# #     content = [PLACEHOLDER_ENTRY["group"]]
# #     return JSONResponse(content=content)
# 
# 
# 
# 
# 
# 
# 
# 
# @app.get("/robots/{path: path}/", response_class=Response)
# async def robots_entry(path:str):
#     return Response(content=f"No data found for {path}.", media_type="application/json")
# 
# 
# @app.get("/robots/group/", response_class=Response)
# async def robots_group(path:str):
#     return Response(content=f"No data found for {path}.", media_type="application/json")
# 
# 
# @app.get("/robots/", response_class=Response)
# async def robots(path:str):
#     return Response(content=f"No data found for {path}.", media_type="application/json")
# 
# @app.get("/head/basic/{path: path}/", response_class=Response)
# async def head_basic(path:str):
#     return Response(content=f"No data found for {path}.", media_type="application/json")
# 
# 
# @app.get("/head/social/{path: path}/", response_class=Response)
# async def head_social(path:str):
#     return Response(content=f"No data found for {path}.", media_type="application/json")
# 
# 
# @app.get("/head/json-dl/{path: path}/", response_class=Response)
# async def head_json_dl(path:str):
#     return Response(content=f"No data found for {path}.", media_type="application/json")


if __name__ == "__main__":
    print("Starting the production server on port", config.PROD_PORT)
    import uvicorn
    uvicorn.run(
        "bin.run:app",
        port=config.PROD_PORT,
        log_level="info",
        reload=False,
    )
