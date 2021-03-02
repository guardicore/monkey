from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class Weblogic(BaseTemplate):

    config_values = BaseTemplate.config_values

    config_values.update({
        "basic.exploiters.exploiter_classes": ["WebLogicExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.18", "10.2.2.19"]
    })
