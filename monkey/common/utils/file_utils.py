import os


class InvalidPath(Exception):
    pass


def expand_path(path: str) -> str:
    if not path:
        raise InvalidPath("Empty path provided")
    return os.path.expandvars(os.path.expanduser(path))
