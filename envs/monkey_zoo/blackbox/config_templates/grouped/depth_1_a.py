from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Depth1A(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)
    # TODO ADD SMB PTH machine
    # Tests:
    # Hadoop
    # Log4shell
    # MSSQL
    # SMB password stealing and brute force
    # SSH password and key brute-force, key stealing
    config_values.update(
        {
            "basic.exploiters.exploiter_classes": [
                "HadoopExploiter",
                "Log4ShellExploiter",
                "MSSQLExploiter",
                "SmbExploiter",
                "SSHExploiter",
            ],
            "basic_network.scope.subnet_scan_list": [
                "10.2.2.2",
                "10.2.2.3",
                "10.2.3.55",
                "10.2.3.56",
                "10.2.3.49",
                "10.2.3.50",
                "10.2.3.51",
                "10.2.3.52",
                "10.2.2.16",
                "10.2.2.14",
                "10.2.2.15",
                "10.2.2.11",
                "10.2.2.12",
            ],
            "basic.credentials.exploit_password_list": ["Ivrrw5zEzs", "Xk8VDTsC", "^NgDvY59~8"],
            "basic.credentials.exploit_user_list": ["m0nk3y"],
            "monkey.system_info.system_info_collector_classes": [
                "MimikatzCollector",
            ],
        }
    )
