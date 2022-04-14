from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class PowerShell(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["PowerShellExploiter"],
            "basic_network.scope.subnet_scan_list": [
                "10.2.3.45",
                "10.2.3.46",
                "10.2.3.47",
                "10.2.3.48",
            ],
            "basic.credentials.exploit_password_list": ["Passw0rd!"],
            "basic_network.scope.depth": 2,
            "basic.credentials.exploit_user_list": ["m0nk3y", "m0nk3y-user"],
            "internal.classes.finger_classes": [],
            "internal.network.tcp_scanner.HTTP_PORTS": [],
            "internal.network.tcp_scanner.tcp_target_ports": [5985, 5986],
            "internal.exploits.exploit_ntlm_hash_list": [
                "d0f0132b308a0c4e5d1029cc06f48692",
            ],
        }
    )
