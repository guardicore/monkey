from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class Struts2(BaseTemplate):

    config_values = BaseTemplate.config_values

    config_values.update({
        "basic.exploiters.exploiter_classes": ["Struts2Exploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.23", "10.2.2.24"]
    })
