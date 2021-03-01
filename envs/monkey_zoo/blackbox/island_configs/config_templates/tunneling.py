from envs.monkey_zoo.blackbox.island_configs.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.island_configs.config_templates.config_template import ConfigValueDescriptor


class Tunneling(BaseTemplate):

    @staticmethod
    def should_run(class_name: str) -> bool:
        return True

    config_value_list = [
        ConfigValueDescriptor("basic.exploiters.exploiter_classes",
                              ["SmbExploiter",
                               "WmiExploiter",
                               "SSHExploiter"
                               ]),
        ConfigValueDescriptor("basic_network.scope.subnet_scan_list",
                              ["10.2.2.9",
                               "10.2.1.10",
                               "10.2.0.11",
                               "10.2.0.12"
                               ]),
        ConfigValueDescriptor("basic.credentials.exploit_password_list",
                              ["Password1!",
                               "3Q=(Ge(+&w]*",
                               "`))jU7L(w}",
                               "t67TC5ZDmz",
                               "12345678"
                               ]),
        ConfigValueDescriptor("basic.credentials.exploit_user_list",
                              ["Administrator",
                               "m0nk3y",
                               "user"
                               ]),
        ConfigValueDescriptor("internal.classes.finger_classes",
                              ["SSHFinger",
                               "PingScanner",
                               "HTTPFinger",
                               "SMBFinger",
                               ])
    ]
