from typing import Optional, List, Union

from pydantic import BaseModel


class DbConstants:
    CATEGORY_TABLE = "category"
    PLACES_TABLE = "places"
    DB_NAME = "city-life-places.db"

class AppConstants:
    DEFAULT_CITY = "bali"
    ALLOWED_CITIES = ["bali", "tokyo"]

class Category(BaseModel):
    id: Optional[int] = -1
    name: str
    emoji: str


class Place(BaseModel):
    id: Optional[int] = -1
    name: str
    category: Union[int, str]
    url: str
    city: Optional[str] = "None"

class CategoryPlaces(BaseModel):
    category_name: str
    category_emoji: str
    places: List[Place]
