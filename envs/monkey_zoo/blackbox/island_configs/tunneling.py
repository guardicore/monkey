from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class Tunneling(BaseTemplate):
    config_values = BaseTemplate.config_values

    config_values.update({
        "basic.exploiters.exploiter_classes": ["SmbExploiter",
                                               "WmiExploiter",
                                               "SSHExploiter"
                                               ],
        "basic_network.scope.subnet_scan_list": ["10.2.2.9",
                                                 "10.2.1.10",
                                                 "10.2.0.11",
                                                 "10.2.0.12"],
        "basic.credentials.exploit_password_list": ["Password1!",
                                                    "3Q=(Ge(+&w]*",
                                                    "`))jU7L(w}",
                                                    "t67TC5ZDmz",
                                                    "12345678"],
        "basic.credentials.exploit_user_list": ["Administrator",
                                                "m0nk3y",
                                                "user"],
        "internal.classes.finger_classes": ["SSHFinger",
                                            "PingScanner",
                                            "HTTPFinger",
                                            "SMBFinger"]
    })
