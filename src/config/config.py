from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "db": {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST"),
    },
    "table": "words"
}