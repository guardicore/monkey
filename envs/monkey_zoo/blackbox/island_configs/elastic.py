from copy import copy

from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.island_configs.config_template import ConfigTemplate


class Elastic(ConfigTemplate):

    config_values = copy(BaseTemplate.config_values)

    config_values.update({
        "basic.exploiters.exploiter_classes": ["ElasticGroovyExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.4", "10.2.2.5"]
    })
