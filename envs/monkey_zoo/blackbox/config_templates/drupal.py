from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Drupal(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "internal.classes.finger_classes": ["HTTPFinger"],
            "basic.exploiters.exploiter_classes": ["DrupalExploiter"],
            "basic_network.scope.subnet_scan_list": ["10.2.2.28"],
            "internal.network.tcp_scanner.HTTP_PORTS": [80],
            "internal.network.tcp_scanner.tcp_target_ports": [],
        }
    )
