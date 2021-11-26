import os
import platform

from monkey_island.cc.server_utils import consts


def test_monkey_island_abs_path():
    assert consts.MONKEY_ISLAND_ABS_PATH.endswith("monkey_island")
    assert os.path.isdir(consts.MONKEY_ISLAND_ABS_PATH)


def test_default_server_config_file_path():
    if platform.system() == "Windows":
        server_file_path = f"{consts.MONKEY_ISLAND_ABS_PATH}\\cc\\{consts.SERVER_CONFIG_FILENAME}"
    else:
        server_file_path = f"{consts.MONKEY_ISLAND_ABS_PATH}/cc/{consts.SERVER_CONFIG_FILENAME}"

    assert consts.PACKAGE_CONFIG_PATH == server_file_path
