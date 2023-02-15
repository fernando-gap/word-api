import os
from collections import deque
from typing import List

def chunk_data(file: str, threads: int = None):
    """Equally split the given size of bytes into a lazy readable stream.

    :param: the file path
    """
    size = os.stat(file).st_size
    cpu = os.cpu_count()

    if not threads and not cpu:
        raise Exception('Cannot determine number of threads')

    if not threads and cpu:
        threads = cpu

    with open(file) as f:
        piece = 0
        offset = size//threads

        while piece < size:
            data = f.readlines(offset)
            if not data:
                break
            yield data
            piece += offset


def split_file(file: str, directory: str = './.split') -> List[str]:
    """Split file in equal parts and save in a directory

    :param file: file to be split
    :param directory: where the files will be saved, if the
        directory does not exists, then it will be
        created, defaults to './.split'.
    :return: "The path of each file"
    """

    if directory.endswith('/'):
        directory = directory[:-1]

    if not os.path.exists(directory):
        os.mkdir(directory)

    filename = os.path.basename(file)
    files = []
    count = 1
    for chunk in chunk_data(file):
        filepath = f'{directory}/{count}-{filename}'
        with open(filepath, 'w+') as f:
            f.writelines(chunk)
            files.append(filepath)
            count += 1
    return files
