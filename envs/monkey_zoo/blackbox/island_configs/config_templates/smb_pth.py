from envs.monkey_zoo.blackbox.island_configs.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.island_configs.config_templates.config_template import ConfigValueDescriptor


class SmbPth(BaseTemplate):

    @staticmethod
    def should_run(class_name: str) -> bool:
        return True

    config_value_list = [
        ConfigValueDescriptor("basic.exploiters.exploiter_classes", ["SmbExploiter"]),
        ConfigValueDescriptor("basic_network.scope.subnet_scan_list",
                              ["10.2.2.15"]),
        ConfigValueDescriptor("basic.credentials.exploit_password_list",
                              ["Password1!",
                               "Ivrrw5zEzs"
                               ]),
        ConfigValueDescriptor("basic.credentials.exploit_user_list",
                              ["Administrator",
                               "m0nk3y",
                               "user"
                               ]),
        ConfigValueDescriptor("internal.classes.finger_classes",
                              ["SMBFinger",
                               "PingScanner",
                               "HTTPFinger"
                               ]),
        ConfigValueDescriptor("internal.classes.exploits.exploit_ntlm_hash_list",
                              ["5da0889ea2081aa79f6852294cba4a5e",
                               "50c9987a6bf1ac59398df9f911122c9b"
                               ])
    ]
