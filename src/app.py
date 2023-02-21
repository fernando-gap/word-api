import os
import asyncio

from aiohttp import ClientSession
from fastapi import BackgroundTasks, FastAPI, UploadFile

import src.utils
from src.db import Database, Download
from src.config import config as conf

app = FastAPI()
threads = os.cpu_count()

def start_requests(file: UploadFile):
    with open(f'/tmp/{file.filename}', 'wb+') as f:
        for line in file.file.readlines():
            f.write(line)

    files = src.utils.split_file(f'/tmp/{file.filename}')
    asyncio.run(main(files, conf))


@app.post("/file")
async def route_file(
        file: UploadFile,
        background_tasks: BackgroundTasks):

    background_tasks.add_task(start_requests, file)
    return {
        "filename": file.filename,
        "size": file.size
    }


async def main(files, conf):
    processes = []

    for file in files:
        processes.append(
            asyncio.ensure_future(
                init_thread(file, conf)
            )
        )

    await asyncio.gather(*processes)

async def init_thread(file, conf):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'}
    async with await Database(**conf["db"]).create() as db:
        async with ClientSession(headers=headers) as session:
            get = Download(conf["table"], db)
            await get.html(file, session)
            print(Download.total)
