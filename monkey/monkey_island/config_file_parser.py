import json


def load_server_config_from_file(server_config_path):
    with open(server_config_path, "r") as f:
        config_content = f.read()
        config = json.loads(config_content)
        return config
