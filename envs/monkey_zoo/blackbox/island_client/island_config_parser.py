import json

import dpath.util

from common.configuration.agent_configuration import AgentConfiguration


class IslandConfigParser:
    @staticmethod
    def get_serialized_config(agent_configuration: AgentConfiguration) -> str:
        return agent_configuration.to_json()

    @staticmethod
    def get_ips_of_targets(raw_config):
        return dpath.util.get(json.loads(raw_config), "basic_network.scope.subnet_scan_list", ".")
