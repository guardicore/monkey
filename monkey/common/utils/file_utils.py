import os


def expand_path(path: str) -> str:
    return os.path.expandvars(os.path.expanduser(path))
