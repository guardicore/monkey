from copy import copy

from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class Drupal(BaseTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update({
        "internal.classes.finger_classes": ["PingScanner", "HTTPFinger"],
        "basic.exploiters.exploiter_classes": ["DrupalExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.28"]
    })
