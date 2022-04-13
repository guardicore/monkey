from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Depth2A(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)
    # SSH password and key brute-force, key stealing (10.2.2.11, 10.2.2.12)
    config_values.update(
        {
            "basic.exploiters.exploiter_classes": [
                "SSHExploiter",
            ],
            "basic_network.scope.subnet_scan_list": [
                "10.2.2.11",
                "10.2.2.12",
            ],
            "basic_network.scope.depth": 2,
            "basic.credentials.exploit_password_list": ["^NgDvY59~8"],
            "basic.credentials.exploit_user_list": ["m0nk3y"],
        }
    )
