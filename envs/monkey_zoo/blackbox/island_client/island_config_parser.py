from typing import Iterable, Mapping

import dpath.util

from common.configuration.agent_configuration import AgentConfiguration


class IslandConfigParser:
    @staticmethod
    def get_serialized_config(agent_configuration: AgentConfiguration) -> str:
        return agent_configuration.to_json()

    @staticmethod
    def get_target_ips_from_configuration(agent_configuration: AgentConfiguration) -> Iterable:
        return agent_configuration.propagation.network_scan.targets.subnets
