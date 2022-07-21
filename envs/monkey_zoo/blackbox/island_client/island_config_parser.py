from typing import Iterable, Mapping

import dpath.util

from common.configuration.agent_configuration import AgentConfiguration


class IslandConfigParser:
    @staticmethod
    def get_serialized_config(agent_configuration: AgentConfiguration) -> str:
        return agent_configuration.to_json()

    @staticmethod
    def get_ips_of_targets(raw_config: Mapping) -> Iterable:
        return dpath.util.get(
            raw_config, "agent_configuration.propagation.network_scan.targets.subnets", "."
        )
