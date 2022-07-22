from typing import Iterable

from envs.monkey_zoo.blackbox.test_configurations.test_configuration import TestConfiguration


def get_target_ips(test_configuration: TestConfiguration) -> Iterable[str]:
    return test_configuration.agent_configuration.propagation.network_scan.targets.subnets
