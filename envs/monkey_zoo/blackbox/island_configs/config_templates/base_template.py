from envs.monkey_zoo.blackbox.island_configs.config_templates.config_template import ConfigTemplate, \
    ConfigValueDescriptor


# Disables a lot of config values not required for a specific feature test
class BaseTemplate(ConfigTemplate):

    @staticmethod
    def should_run(class_name: str) -> bool:
        return False

    config_value_list = [
        ConfigValueDescriptor("basic.exploiters.exploiter_classes", []),
        ConfigValueDescriptor("basic_network.scope.local_network_scan", False),
        ConfigValueDescriptor("internal.classes.finger_classes",
                              ["PingScanner", "HTTPFinger"]),
        ConfigValueDescriptor("internal.monkey.system_info.system_info_collector_classes",
                              ["EnvironmentCollector", "HostnameCollector"])
    ]
