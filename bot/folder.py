import os

from . import BASE_FOLDER

storage = BASE_FOLDER


def reset():
    global storage
    storage = BASE_FOLDER


def set(path: str):
    global storage
    storage = os.path.join(BASE_FOLDER, path)
    try:
        os.mkdir(storage)
    except FileExistsError:
        pass


def getPath() -> str:
    return storage.replace(BASE_FOLDER, "", 1) or "/"


def get() -> str:
    return storage
