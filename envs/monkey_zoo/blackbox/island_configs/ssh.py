from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class Ssh(BaseTemplate):
    config_values = BaseTemplate.config_values

    config_values.update({
        "basic.exploiters.exploiter_classes": ["SSHExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.11",
                                                 "10.2.2.12"],
        "basic.credentials.exploit_password_list": ["Password1!",
                                                    "12345678",
                                                    "^NgDvY59~8"],
        "basic.credentials.exploit_user_list": ["Administrator",
                                                "m0nk3y",
                                                "user"],
        "internal.classes.finger_classes": ["SSHFinger",
                                            "PingScanner",
                                            "HTTPFinger"]
    })
