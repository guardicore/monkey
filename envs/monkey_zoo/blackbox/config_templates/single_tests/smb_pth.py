from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class SmbPth(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["SmbExploiter"],
            "basic_network.scope.subnet_scan_list": ["10.2.2.15"],
            "basic.credentials.exploit_password_list": ["Password1!", "Ivrrw5zEzs"],
            "basic.credentials.exploit_user_list": ["Administrator", "m0nk3y", "user"],
            "internal.classes.finger_classes": ["SMBFinger", "HTTPFinger"],
            "internal.network.tcp_scanner.HTTP_PORTS": [],
            "internal.network.tcp_scanner.tcp_target_ports": [445],
            "internal.classes.exploits.exploit_ntlm_hash_list": [
                "5da0889ea2081aa79f6852294cba4a5e",
                "50c9987a6bf1ac59398df9f911122c9b",
            ],
        }
    )
