from copy import copy

from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class SmbMimikatz(BaseTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update({
        "basic.exploiters.exploiter_classes": ["SmbExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.14", "10.2.2.15"],
        "basic.credentials.exploit_password_list": ["Password1!", "Ivrrw5zEzs"],
        "basic.credentials.exploit_user_list": ["Administrator", "m0nk3y", "user"],
        "internal.classes.finger_classes": ["SMBFinger", "PingScanner", "HTTPFinger"],
        "monkey.system_info.system_info_collector_classes": ["EnvironmentCollector",
                                                             "HostnameCollector",
                                                             "ProcessListCollector",
                                                             "MimikatzCollector"]
    })
