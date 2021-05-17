import os

from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR


def create_data_dir(data_dir: str) -> None:
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir, mode=0o700)


def create_default_data_dir() -> None:
    if not os.path.isdir(DEFAULT_DATA_DIR):
        os.mkdir(DEFAULT_DATA_DIR, mode=0o700)
