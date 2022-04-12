from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Zerologon(ConfigTemplate):

    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["ZerologonExploiter", "SmbExploiter"],
            "basic_network.scope.subnet_scan_list": ["10.2.2.25"],
            # Empty list to make sure ZeroLogon adds "Administrator" username
            "basic.credentials.exploit_user_list": [],
            "internal.network.tcp_scanner.HTTP_PORTS": [],
            "internal.network.tcp_scanner.tcp_target_ports": [135, 445],
        }
    )
