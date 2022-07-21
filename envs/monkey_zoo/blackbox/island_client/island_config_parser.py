from typing import Iterable

from common.configuration.agent_configuration import AgentConfiguration


class IslandConfigParser:
    @staticmethod
    def get_target_ips_from_configuration(agent_configuration: AgentConfiguration) -> Iterable:
        return agent_configuration.propagation.network_scan.targets.subnets
