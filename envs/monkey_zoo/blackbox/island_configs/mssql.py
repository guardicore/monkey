from copy import copy

from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class Mssql(BaseTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update({
        "basic.exploiters.exploiter_classes": ["MSSQLExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.16"],
        "basic.credentials.exploit_password_list": ["Password1!",
                                                    "Xk8VDTsC",
                                                    "password",
                                                    "12345678"],
        "basic.credentials.exploit_user_list": ["Administrator",
                                                "m0nk3y",
                                                "user"]
    })
