from typing import List

from server.constants import Category, Place
from server.database_handler import DataBaseHandler
from server.utils import get_formatted_category, get_formatted_place_category


class PlaceCategoryService:
    def __init__(self, db_name):
        self.db_conn = DataBaseHandler(db_name)

    def insert_category(self, items: List[Category]):
        insert_data = [(item.name, item.emoji) for item in items]
        print(f"IN {__name__}.insert_category  for len={len(insert_data)}")
        self.db_conn.insert_category(insert_data)

    def insert_place(self, items: List[Place]):
        insert_data = [(item.name, item.city.upper(), item.category, item.url) for item in items]
        print(f"IN {__name__}.insert_place for len={len(insert_data)}")
        self.db_conn.insert_places(insert_data)

    def ops_fetch_all_category(self):
        db_rows = self.db_conn.ops_fetch_all_category()
        output = get_formatted_category(db_rows)
        return output

    def fetch_places_category(self, city: str = None):
        db_rows = self.db_conn.fetch_places_grouped_by_category(city)
        output = get_formatted_place_category(db_rows)
        return output


