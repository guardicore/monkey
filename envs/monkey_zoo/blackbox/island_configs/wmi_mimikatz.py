from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class WmiMimikatz(BaseTemplate):
    config_values = BaseTemplate.config_values

    config_values.update({
        "basic.exploiters.exploiter_classes": ["WmiExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.14",
                                                 "10.2.2.15"],
        "basic.credentials.exploit_password_list": ["Password1!",
                                                    "Ivrrw5zEzs"],
        "basic.credentials.exploit_user_list": ["Administrator",
                                                "m0nk3y",
                                                "user"],
        "monkey.system_info.system_info_collector_classes": ["EnvironmentCollector",
                                                             "HostnameCollector",
                                                             "ProcessListCollector",
                                                             "MimikatzCollector"]
    })
