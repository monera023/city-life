import os
from typing import List, Annotated

from fastapi import FastAPI, Request, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

from server.constants import DbConstants, Category, Place, AppConstants
from server.places_category_service import PlaceCategoryService
from server.utils import validate_city

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
        allowed_get_endpoints = ["/", "/bali_bg_image.jpeg", "/tokyo_bg_image.jpeg", "/ops-fetch", "/_ops/category_all", "/bali", "/Bali", "/BALI",
                                 "/tokyo", "/Tokyo", "/TOKYO"]
        if request.query_params or request.method == "POST":
            print(f"HERE... for {request.url} and method = {request.method}")
            return JSONResponse(
                status_code=403,
                content={"detail": "Access forbidden"}
            )
        # Check if the request is GET and the path is in the allowed list
        if request.method == "GET" and request.url.path in allowed_get_endpoints:
            response = await call_next(request)
            return response

        # If not allowed, return a 403 Forbidden response
        return JSONResponse(
            status_code=403,
            content={"detail": "Access forbidden"}
        )

app.add_middleware(RestrictAccessMiddleware)


@app.get("/bali_bg_image.jpeg")
async def server_bg_image():
    return FileResponse("static_files/bali_bg_image.jpeg", media_type="image/jpeg")

@app.get("/tokyo_bg_image.jpeg")
async def server_bg_image():
    return FileResponse("static_files/tokyo_bg_image.jpeg", media_type="image/jpeg")


@app.get("/{city}")
async def fetch(request: Request, city: Annotated[str, Path(title="City to filter on")]):
    if not validate_city(city):
        return JSONResponse(
            status_code=403,
            content={"detail": "Access forbidden"}
        )
    print(f"IN fetch city for={city}")
    items = place_category_service.fetch_places_category(city.upper())
    return templates.TemplateResponse(f"fetch_{city.lower()}.html", {"request": request, "categories": items, "city": city.upper()})


@app.get("/")
async def fetch(request: Request):
    print(f"IN fetch..")
    items = place_category_service.fetch_places_category()
    return templates.TemplateResponse(f"fetch_{AppConstants.DEFAULT_CITY}.html", {"request": request, "categories": items, "city": AppConstants.DEFAULT_CITY.upper()})

@app.get("/_ops/ops-fetch")
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