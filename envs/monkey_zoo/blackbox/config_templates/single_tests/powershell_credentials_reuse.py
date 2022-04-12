from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class PowerShellCredentialsReuse(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["PowerShellExploiter"],
            "basic_network.scope.subnet_scan_list": [
                "10.2.3.46",
            ],
            "basic_network.scope.depth": 2,
            "internal.classes.finger_classes": [],
            "internal.network.tcp_scanner.HTTP_PORTS": [],
            "internal.network.tcp_scanner.tcp_target_ports": [5985, 5986],
        }
    )
