from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class WmiMimikatz(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["WmiExploiter"],
            "basic_network.scope.subnet_scan_list": ["10.2.2.14", "10.2.2.15"],
            "basic.credentials.exploit_password_list": ["Password1!", "Ivrrw5zEzs"],
            "basic.credentials.exploit_user_list": ["Administrator", "m0nk3y", "user"],
            "internal.network.tcp_scanner.HTTP_PORTS": [],
            "internal.network.tcp_scanner.tcp_target_ports": [135],
            "monkey.system_info.system_info_collector_classes": [
                "MimikatzCollector",
            ],
        }
    )
