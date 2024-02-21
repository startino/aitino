import logging
import os
import asyncio
from pathlib import Path
import json

import sqlite3

logger = logging.getLogger("root")


class CacheService:
    def __init__(self, seed: int = 41):
        self.path = Path(os.getcwd(), ".cache", str(seed), "cache.db")
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.json = None

        print(f"CacheService started with seed {seed}")

    def get_as_json(self):
        self.cursor.execute("SELECT * FROM Cache;")
        cache = self.cursor.fetchall()
        cache_json = []
        for row in cache:
            cache_json.append({"id": row[0], "data": json.loads(row[1])})

        return cache_json

    def poll_cache(self):
        new_json = self.get_as_json()

        self.json = new_json
        return self.json
