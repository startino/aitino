import logging
import os
from pathlib import Path
import json

import sqlite3

logger = logging.getLogger("root")


class CacheService:
    def __init__(self, seed: int = 41, collection: str = "groupchat"):
        self.path = Path(os.getcwd(), ".cache", str(seed), "cache.db")
        print(os.path.exists(self.path))
        print(self.path)
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def get_as_json(self):
        # List all tables
        # Get a list of tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()

        # Inspect the "Cache" table
        if "Cache" in (table[0] for table in tables):
            self.cursor.execute("PRAGMA table_info(Cache);")
            columns_cache = self.cursor.fetchall()

            # Print the columns for "Cache" table
            print("\nColumns for 'Cache' table:")
            for column in columns_cache:
                print(f"{column[1]} - {column[2]}")

        # Inspect the "Settings" table
        if "Settings" in (table[0] for table in tables):
            self.cursor.execute("PRAGMA table_info(Settings);")
            columns_settings = self.cursor.fetchall()

            # Print the columns for "Settings" table
            print("\nColumns for 'Settings' table:")
            for column in columns_settings:
                print(f"{column[1]} - {column[2]}")

        # Print whole cache table
        self.cursor.execute("SELECT * FROM Cache;")
        cache = self.cursor.fetchall()
        # make table json
        cache_json = []
        for row in cache:
            cache_json.append(
                {"id": row[0], "data": json.loads(row[1]), "timestamp": row[2]}
            )

        return cache_json
