import psycopg
import requests

class Database:
    def __init__(self, *, dbname: str, user: str, password: str, host: str):
        self.connection_string = f"dbname={dbname} user={user} password={password} host={host}"

    def create(self, *args) -> psycopg.Connection:
        """Create a postgres connection.
        """
        return psycopg.connect(self.connection_string, *args)


class Download:
    total = 0

    def __init__(self, table: str, connection: psycopg.Connection):
        self.db = connection
        self.table = table

    def html(self, url: str, word: str) -> str:
        req = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
        })

        with self.db.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {self.table} (site, word, html) 
                VALUES (%s, %s, %s)
                """, (url, word, req.text))
        
        Download.total += 1
        self.db.commit()