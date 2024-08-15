import sqlite3
from typing import List, Tuple

from server.constants import DbConstants


class DataBaseHandler:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.setup_done = False
        self.do_setup()

    def do_setup(self):
        if self.setup_done:
            print(f"Setup already done..")
        else:
            tables = [DbConstants.CATEGORY_TABLE, DbConstants.PLACES_TABLE]
            tables_in_query = ", ".join('?' for _ in tables)
            check_table_query = f"select name from sqlite_master where type='table' and name in ({tables_in_query})"
            cursor = self.db.cursor()
            cursor.execute(check_table_query, tables)

            tables_exist = cursor.fetchall()
            if len(tables_exist) == len(tables):
                print(f"Tables present..")
            else:
                print(f"Doing setup..")
                self.create_tables()

    def create_tables(self):
        print(f"In create_tables..")
        try:
            cursor = self.db.cursor()
            create_category_table_query = '''
             CREATE TABLE IF NOT EXISTS category (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              category_name TEXT,
              category_emoji TEXT
             )
            '''
            cursor.execute(create_category_table_query)
            self.db.commit()

            create_places_table_query = '''
             CREATE TABLE IF NOT EXISTS places (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              city TEXT,
              category INTEGER,
              url TEXT
             )
            '''
            cursor.execute(create_places_table_query)
            self.db.commit()
            cursor.close()
            self.setup_done = True
        except Exception as e:
            print(f"Got exception while creating tables= {e}")
            raise e


    def insert_category(self, items: List[Tuple]):
        print(f"IN insert_category")
        try:
            cursor = self.db.cursor()
            insert_category_query = f"INSERT INTO {DbConstants.CATEGORY_TABLE} (category_name, category_emoji) VALUES (?, ?)"
            cursor.executemany(insert_category_query, items)
            self.db.commit()
            cursor.close()
        except Exception as e:
            print(f"Got exception while inserting into category table = {e}")
            raise e

    def insert_places(self, items: List[Tuple]):
        print(f"In insert_places")
        try:
            cursor = self.db.cursor()
            insert_places_query = f"INSERT INTO {DbConstants.PLACES_TABLE} (name, city, category, url) VALUES (?, ?, ?, ?)"
            cursor.executemany(insert_places_query, items)
            self.db.commit()
            cursor.close()
        except Exception as e:
            print(f"Got exception while inserting in places tables = {e}")
            raise e

    def fetch_places_grouped_by_category(self, city: str = None):
        print(f"IN fetch_places_grouped_by_category")
        try:
            cursor = self.db.cursor()
            select_query = (f"select c.category_name, c.category_emoji, p.name, p.url from category as c right join"
                            f" places as p on c.id = p.category")
            if city is not None:
                select_query += f" where p.city = '{city}'"
            cursor.execute(select_query)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print(f"Got exception in fetch_places_grouped_by_category = {e}")
            raise e


    def ops_fetch_all_category(self):
        print(f"In _ops_fetch_all_category")
        try:
            cursor = self.db.cursor()
            fetch_all_category_query = f"select * from {DbConstants.CATEGORY_TABLE}"
            cursor.execute(fetch_all_category_query)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print(f"Got exception in _ops_fetch_all_category = {e}")
            raise e

    def flush_table(self, table_name):
        cursor = self.db.cursor()
        flush_table_query = f"DELETE FROM {table_name}"
        cursor.execute(flush_table_query)

        reset_autoincre_query = f"DELETE FROM sqlite_sequence WHERE name = '{table_name}'"
        cursor.execute(reset_autoincre_query)

        self.db.commit()
        cursor.close()
        print("Done flush for table..")

    def drop_table(self, table_name):
        cursor = self.db.cursor()
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(drop_table_query)
        self.db.commit()
        cursor.close()
        print(f"Dropped table..{table_name} from db")

    def get_data(self, table_name):
        cursor = self.db.cursor()

        select_all_query = f"SELECT * FROM {table_name}"
        cursor.execute(select_all_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
