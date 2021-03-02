from copy import copy

from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class Hadoop(BaseTemplate):

    config_values = copy(BaseTemplate.config_values)

    config_values.update({
        "basic.exploiters.exploiter_classes": ["HadoopExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.2", "10.2.2.3"]
    })
