import os
import threading
from io import BytesIO

import utils
from db import Database, Download
from fastapi import FastAPI, UploadFile


app = FastAPI()
threads = os.cpu_count()

conf = {
    "db": {
        "dbname": "postgres",
        "user": "postgres",
        "password": "adm",
        "host": "172.17.0.2"
    },
    "table": "word"
}

with Database(**conf['db']).create() as db:
    with db.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS WORDS (
            word VARCHAR(50) PRIMARY KEY,
            site VARCHAR NOT NULL,
            html TEXT NOT NULL
        )
        """)

@app.post("/file")
def route_file(file: UploadFile):
    with open(f'/tmp/{file.filename}', 'wb+') as f:
        for line in file.file.readlines():
            f.write(line)
    
    files = utils.split_file(f'/tmp/{file.filename}')
    threads_list = create_thread(files, conf)

    for thread in threads_list:
        thread.start()
        
    return { "filename": file.filename, "size": file.size, "threads": len(files)}


def create_thread(files, conf):
    threads_list = []

    for file in files:
        threads_list.append(
            threading.Thread(target=init_thread, 
            args=[file, conf]))

    return threads_list


def init_thread(file, conf):
    con = Database(**conf["db"]).create()
    with open(file) as f:
        get = Download(conf["table"], con)
        for line in f.readlines():
            url, word = line.split(',')
            get.html(url, word)
    con.close()

