from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Ssh(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["SSHExploiter"],
            "basic_network.scope.subnet_scan_list": ["10.2.2.11", "10.2.2.12"],
            "basic.credentials.exploit_password_list": ["Password1!", "12345678", "^NgDvY59~8"],
            "basic_network.scope.depth": 2,
            "basic.credentials.exploit_user_list": ["Administrator", "m0nk3y", "user"],
            "internal.classes.finger_classes": ["SSHFinger"],
            "internal.network.tcp_scanner.HTTP_PORTS": [],
            "internal.network.tcp_scanner.tcp_target_ports": [22],
        }
    )
