from envs.monkey_zoo.blackbox.island_configs.config_templates.config_template import ConfigValueDescriptor, \
    ConfigTemplate


class Performance(ConfigTemplate):

    @staticmethod
    def should_run(class_name: str) -> bool:
        return True

    config_value_list = [
        ConfigValueDescriptor("basic.credentials.exploit_password_list",
                              ["Xk8VDTsC",
                               "^NgDvY59~8",
                               "Ivrrw5zEzs",
                               "3Q=(Ge(+&w]*",
                               "`))jU7L(w}",
                               "t67TC5ZDmz"
                               ]),
        ConfigValueDescriptor("basic.credentials.exploit_user_list",
                              ["m0nk3y"
                               ]),
        ConfigValueDescriptor("basic.exploiters.exploiter_classes",
                              ["SmbExploiter",
                               "WmiExploiter",
                               "SSHExploiter",
                               "ShellShockExploiter",
                               "SambaCryExploiter",
                               "ElasticGroovyExploiter",
                               "Struts2Exploiter",
                               "WebLogicExploiter",
                               "HadoopExploiter",
                               "VSFTPDExploiter",
                               "MSSQLExploiter",
                               "ZerologonExploiter"
                               ]),
        ConfigValueDescriptor("basic_network.network_analysis.inaccessible_subnets",
                              ["10.2.2.0/30",
                               "10.2.2.8/30",
                               "10.2.2.24/32",
                               "10.2.2.23/32",
                               "10.2.2.21/32",
                               "10.2.2.19/32",
                               "10.2.2.18/32",
                               "10.2.2.17/32"
                               ]),
        ConfigValueDescriptor("basic_network.scope.subnet_scan_list",
                              ["10.2.2.2",
                               "10.2.2.3",
                               "10.2.2.4",
                               "10.2.2.5",
                               "10.2.2.8",
                               "10.2.2.9",
                               "10.2.1.10",
                               "10.2.0.11",
                               "10.2.0.12",
                               "10.2.2.11",
                               "10.2.2.12",
                               "10.2.2.14",
                               "10.2.2.15",
                               "10.2.2.16",
                               "10.2.2.18",
                               "10.2.2.19",
                               "10.2.2.20",
                               "10.2.2.21",
                               "10.2.2.23",
                               "10.2.2.24",
                               "10.2.2.25",
                               ])

    ]
