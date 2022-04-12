from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Depth4A(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    # Tests:
    # Powershell
    # Tunneling (SSH brute force)
    # WMI mimikatz password stealing
    config_values.update(
        {
            "basic.exploiters.exploiter_classes": [
                "PowerShellExploiter",
                "SSHExploiter",
                "WmiExploiter",
            ],
            "basic_network.scope.subnet_scan_list": [
                "10.2.3.45",
                "10.2.3.46",
                "10.2.3.47",
                "10.2.3.48",
                "10.2.2.9",
                "10.2.1.10",
                "10.2.0.12",
                "10.2.0.11",
                "10.2.2.15",
            ],
            "basic.credentials.exploit_password_list": [
                "Passw0rd!",
                "3Q=(Ge(+&w]*",
                "`))jU7L(w}",
                "t67TC5ZDmz" "Ivrrw5zEzs",
            ],
            "basic_network.scope.depth": 3,
            "internal.general.keep_tunnel_open_time": 20,
            "basic.credentials.exploit_user_list": ["m0nk3y", "m0nk3y-user"],
            "internal.network.tcp_scanner.HTTP_PORTS": [],
            "internal.exploits.exploit_ntlm_hash_list": [
                "5da0889ea2081aa79f6852294cba4a5e",
                "50c9987a6bf1ac59398df9f911122c9b",
            ],
            "internal.network.tcp_scanner.tcp_target_ports": [5985, 5986, 22, 135],
        }
    )
