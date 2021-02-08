import platform
import monkey_island.cc.consts as consts


def test_default_server_config_file_path():
    if platform.system() == "Windows":
        server_file_path = consts.MONKEY_ISLAND_ABS_PATH + r"\cc\server_config.json"
    else:
        server_file_path = consts.MONKEY_ISLAND_ABS_PATH + "/cc/server_config.json"

    assert consts.DEFAULT_SERVER_CONFIG_PATH == server_file_path
