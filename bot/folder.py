from . import BASE_FOLDER

_dfolder: str = BASE_FOLDER


def set(f: str):
    global _dfolder
    _dfolder = f


def get() -> str:
    return _dfolder
