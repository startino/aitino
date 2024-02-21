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
        self.loop = asyncio.get_event_loop()

        print(f"CacheService started with seed {seed}")

        self.loop.create_task(self.start_poller())
        print("Poller started")

    def on_change(self):
        print(f"Update hook called, new json has arrived!!")

    def get_as_json(self):
        self.cursor.execute("SELECT * FROM Cache;")
        cache = self.cursor.fetchall()
        cache_json = []
        for row in cache:
            cache_json.append({"id": row[0], "data": json.loads(row[1])})

        return cache_json

    async def start_poller(self):
        while self.connection:
            print("Polling for changes...", end="")
            await asyncio.sleep(0.5)
            new_json = self.get_as_json()

            if new_json != self.json:
                self.json = new_json
                self.on_change()
