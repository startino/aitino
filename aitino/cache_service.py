import logging
import os
from pathlib import Path

import sqlite3
import chromadb

logger = logging.getLogger("root")


class CacheService:
    def __init__(self, seed: int = 41, collection: str = "groupchat"):
        self.path = Path(os.getcwd(), "aitino", ".cache", str(seed), "cache.db")
        print(os.path.exists(self.path))
        print(self.path)
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def get_all(self):
        # List all tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
