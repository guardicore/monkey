import platform

import monkey_island.cc.server_utils.consts as consts


def test_default_server_config_file_path():
    if platform.system() == "Windows":
        server_file_path = f"{consts.DEFAULT_DATA_DIR}\\{consts.SERVER_CONFIG_FILENAME}"
    else:
        server_file_path = f"{consts.DEFAULT_DATA_DIR}/{consts.SERVER_CONFIG_FILENAME}"

    assert consts.DEFAULT_SERVER_CONFIG_PATH == server_file_path
