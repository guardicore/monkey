from copy import copy

from envs.monkey_zoo.blackbox.config_templates.base_template import BaseTemplate
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate


class Tunneling(ConfigTemplate):
    config_values = copy(BaseTemplate.config_values)

    config_values.update(
        {
            "basic.exploiters.exploiter_classes": ["SmbExploiter", "WmiExploiter", "SSHExploiter"],
            "basic_network.scope.subnet_scan_list": [
                "10.2.2.9",
                "10.2.1.10",
                "10.2.0.12",
                "10.2.0.11",
            ],
            "basic_network.scope.depth": 3,
            "internal.general.keep_tunnel_open_time": 150,
            "basic.credentials.exploit_password_list": [
                "Password1!",
                "3Q=(Ge(+&w]*",
                "`))jU7L(w}",
                "t67TC5ZDmz",
                "12345678",
            ],
            "basic.credentials.exploit_user_list": ["Administrator", "m0nk3y", "user"],
            "internal.classes.finger_classes": [
                "SSHFinger",
                "HTTPFinger",
                "SMBFinger",
            ],
        }
    )
