from psycopg import AsyncConnection, Connection
from aiohttp import ClientSession
import asyncio

import os
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self, *,
            dbname: str, user: str, password: str,
            host: str):

        self.connection_string = f"dbname={dbname} user={user} password={password} host={host}"

    def create(self, *args) -> AsyncConnection:
        """Create a postgres async. connection.
        """
        return AsyncConnection.connect(self.connection_string, *args)
    def create_sync(self, *args) -> Connection:
        """Create a postgres sync. connection.
        """
        return Connection.connect(self.connection_string, *args)



class Download:
    total = 0

    def __init__(self,
            table: str,
            connection: AsyncConnection):

        self.db = connection
        self.table = table

    async def fetch(self,
            url: str,
            word: str,
            session: ClientSession):

        async with session.get(url) as resp:
            return await resp.text(), url, word

    async def html(self,
            file: str,
            session: ClientSession) -> str:

        tasks = []
        with open(file) as f:
            for line in f.readlines():
                url, word = line.split(',')
                task = asyncio.ensure_future(self.fetch(url, word.strip('\n'), session))
                tasks.append(task)

        response = await asyncio.gather(*tasks)

        async with self.db.cursor() as cur:
            await cur.executemany(f"""
                INSERT INTO {self.table} (html, site, word)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                """, response)

        Download.total += len(tasks)
        await self.db.commit()
        response = []
        tasks = []
