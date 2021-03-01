from envs.monkey_zoo.blackbox.island_configs.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.island_configs.config_templates.config_template import ConfigValueDescriptor


class Elastic(BaseTemplate):

    @staticmethod
    def should_run(class_name: str) -> bool:
        return True

    config_value_list = [
        ConfigValueDescriptor("basic.exploiters.exploiter_classes", ["ElasticGroovyExploiter"]),
        ConfigValueDescriptor("basic_network.scope.subnet_scan_list", ["10.2.2.4", "10.2.2.5"])
    ]
