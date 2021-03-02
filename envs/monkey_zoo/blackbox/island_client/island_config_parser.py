import json

import dpath.util
from typing_extensions import Type

from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.island_configs.config_template import ConfigTemplate


class IslandConfigParser:

    @staticmethod
    def get_raw_config(config_template: Type[ConfigTemplate],
                       island_client: MonkeyIslandClient) -> str:
        response = island_client.get_config()
        config = IslandConfigParser.apply_template_to_config(config_template, response['configuration'])
        return json.dumps(config)

    @staticmethod
    def apply_template_to_config(config_template: Type[ConfigTemplate],
                                 config: dict) -> dict:
        for path, value in config_template.config_values.items():
            dpath.util.set(config, path, value, '.')
        return config

    @staticmethod
    def get_ips_of_targets(raw_config):
        return dpath.util.get(json.loads(raw_config),
                              "basic_network.scope.subnet_scan_list",
                              '.')
