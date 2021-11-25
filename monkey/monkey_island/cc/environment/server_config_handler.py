import json

from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def load_server_config_from_file(server_config_path) -> IslandConfigOptions:
    with open(server_config_path, "r") as f:
        config_content = f.read()
        config = json.loads(config_content)

        return IslandConfigOptions(config)
