import os
from typing import List

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

from server.constants import DbConstants, Category, Place
from server.places_category_service import PlaceCategoryService

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

place_category_service = PlaceCategoryService(DbConstants.DB_NAME)

origin_str = os.getenv('ORIGINS')
origins = origin_str.split(",")
print(f"here len={len(origins)} and origins= {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_methods=["GET"],
    allow_headers=["*"],
)

class RestrictAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # List of allowed GET endpoints
        allowed_get_endpoints = ["/", "/bg-image.jpeg", "/ops-fetch", "/_ops/category_all"]
        allowed_put_endpoints = ["/_ops/addCategory", "/_ops/addPlace"]
        if request.query_params:
            print(f"HERE... for {request.url} and method = {request.method}")
            return JSONResponse(
                status_code=403,
                content={"detail": "Access forbidden"}
            )
        # Check if the request is GET and the path is in the allowed list
        if request.method == "GET" and request.url.path in allowed_get_endpoints:
            response = await call_next(request)
            return response

        if request.method == "POST" and request.url.path in allowed_put_endpoints:
            response = await call_next(request)
            return response

        # If not allowed, return a 403 Forbidden response
        return JSONResponse(
            status_code=403,
            content={"detail": "Access forbidden"}
        )

app.add_middleware(RestrictAccessMiddleware)


@app.get("/bg-image.jpeg")
async def server_bg_image():
    return FileResponse("static_files/bg-image.jpeg", media_type="image/jpeg")


@app.get("/")
async def fetch(request: Request):
    print(f"IN fetch..")
    items = place_category_service.fetch_places_category()
    return templates.TemplateResponse("fetch.html", {"request": request, "categories": items})

@app.get("/ops-fetch")
async def ops_fetch():
    print(f"IN fetch..")
    items = place_category_service.fetch_places_category()
    return items

@app.get("/_ops/category_all")
async def fetch_all_category():
    print(f"IN fetch_all_category")
    items = place_category_service.ops_fetch_all_category()
    return items

@app.post("/_ops/addCategory")
async def add_category(items: List[Category]):
    print(f"IN add_category")
    place_category_service.insert_category(items)
    return {
        "response": "Added categories.."
    }

@app.post("/_ops/addPlace")
async def add_place(items: List[Place]):
    print(f"In add_place")
    place_category_service.insert_place(items)
    return {
        "response": "Added places.."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)