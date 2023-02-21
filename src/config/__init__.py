from src.db import Database
from .config import config

def init():
    with Database(**config['db']).create_sync() as db:
        with db.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS WORDS (
                word VARCHAR(50) PRIMARY KEY,
                site VARCHAR NOT NULL,
                html TEXT NOT NULL
            )
            """)

init()