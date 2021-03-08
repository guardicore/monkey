from copy import copy

from envs.monkey_zoo.blackbox.island_configs.base_template import BaseTemplate


class ZeroLogon(BaseTemplate):

    config_values = copy(BaseTemplate.config_values)

    config_values.update({
        "basic.exploiters.exploiter_classes": ["ZerologonExploiter"],
        "basic_network.scope.subnet_scan_list": ["10.2.2.25"],
        # Empty list to make sure ZeroLogon adds "Administrator" username
        "basic.credentials.exploit_user_list": []
    })
