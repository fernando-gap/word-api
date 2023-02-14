import os
import threading

import utils
from db import Database, Download


def init_thread(file, conf):
    con = Database(**conf["db"]).create()
    with open(file) as f:
        get = Download(conf["table"], con)
        for line in f.readlines():
            url, word = line.split(',')
            get.html(url, word)
    con.close()

threads = os.cpu_count()
threads_list = []
files = utils.split_file('')

conf = {
    "db": {
        "dbname": "",
        "user": "",
        "password": "",
        "host": ""
    },
    "table": ""
}

for file in files:
    threads_list.append(threading.Thread(
        target=init_thread,
        args=[file, conf]
    ))

for thread in threads_list:
    thread.start()