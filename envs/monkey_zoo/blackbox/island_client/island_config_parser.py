import json

import dpath.util
from typing_extensions import Type

from common.configuration.agent_configuration import AgentConfiguration
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient


class IslandConfigParser:
    @staticmethod
    def get_serialized_config(
        agent_configuration: AgentConfiguration, island_client: MonkeyIslandClient
    ) -> str:
        return agent_configuration.to_json()

    @staticmethod
    def apply_template_to_config(config_template: Type[ConfigTemplate], config: dict) -> dict:
        for path, value in config_template.config_values.items():
            dpath.util.set(config, path, value, ".")
        return config

    @staticmethod
    def get_ips_of_targets(raw_config):
        return dpath.util.get(json.loads(raw_config), "basic_network.scope.subnet_scan_list", ".")
