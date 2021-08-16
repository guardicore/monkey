from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class ShellShock(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["ShellShockExploiter"],
            "basic_network.scope.subnet_scan_list": ["10.2.2.8"],
            "internal.network.tcp_scanner.HTTP_PORTS": [80, 8080],
            "internal.network.tcp_scanner.tcp_target_ports": [],
        }
    )
