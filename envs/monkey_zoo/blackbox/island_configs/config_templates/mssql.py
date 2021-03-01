from envs.monkey_zoo.blackbox.island_configs.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.island_configs.config_templates.config_template import ConfigValueDescriptor


class Mssql(BaseTemplate):

    @staticmethod
    def should_run(class_name: str) -> bool:
        return True

    config_value_list = [
        ConfigValueDescriptor("basic.exploiters.exploiter_classes", ["MSSQLExploiter"]),
        ConfigValueDescriptor("basic_network.scope.subnet_scan_list", ["10.2.2.16"]),
        ConfigValueDescriptor("basic.credentials.exploit_password_list",
                              ["Password1!",
                               "Xk8VDTsC",
                               "password",
                               "12345678"
                               ]),
        ConfigValueDescriptor("basic.credentials.exploit_user_list",
                              ["Administrator",
                               "m0nk3y",
                               "user"
                               ])
    ]
