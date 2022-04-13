from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Depth1B(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)
    # Tests:
    # WMI password login and mimikatz credential stealing (10.2.2.14 and 10.2.2.15)
    # Zerologon
    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["WmiExploiter", "ZerologonExploiter"],
            "basic_network.scope.subnet_scan_list": ["10.2.2.25", "10.2.2.14", "10.2.2.15"],
            "basic.credentials.exploit_password_list": ["Ivrrw5zEzs"],
            "basic.credentials.exploit_user_list": ["m0nk3y"],
            "monkey.system_info.system_info_collector_classes": [
                "MimikatzCollector",
            ],
        }
    )
