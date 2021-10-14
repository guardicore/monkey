from monkey_island.cc.server_utils.file_utils import create_secure_directory


def setup_data_dir(path: str):
    create_secure_directory(path)
