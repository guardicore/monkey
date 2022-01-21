from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Log4jLogstash(ConfigTemplate):

    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["Log4ShellExploiter"],
            "basic_network.scope.subnet_scan_list": ["10.2.3.55", "10.2.3.56"],
        }
    )
