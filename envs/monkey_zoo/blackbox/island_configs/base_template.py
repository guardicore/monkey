from envs.monkey_zoo.blackbox.island_configs.config_template import ConfigTemplate


# Disables a lot of config values not required for a specific feature test
class BaseTemplate(ConfigTemplate):

    config_values = {
        "basic.exploiters.exploiter_classes": [],
        "basic_network.scope.local_network_scan": False,
        "internal.classes.finger_classes": ["PingScanner", "HTTPFinger"],
        "internal.monkey.system_info.system_info_collector_classes":
            ["EnvironmentCollector", "HostnameCollector"],
        "monkey.post_breach.post_breach_actions": []
    }
