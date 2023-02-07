import os
from collections import deque
from typing import List

def chunk_data(file: str):
    """Equally split the given size of bytes into a lazy readable stream.

    :param: the file path
    """
    size = os.stat(file).st_size

    with open(file) as f:
        piece = 0
        offset = size//os.cpu_count()
        print(offset)

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

    filename = os.path.basename(file)
    files = []
    count = 1
    for chunk in chunk_data(file):
        filepath = f'{directory}/{count}-{filename}'
        with open(filepath, 'a') as f:
            f.writelines(chunk)
            files.append(filepath)
            count += 1
    return files
