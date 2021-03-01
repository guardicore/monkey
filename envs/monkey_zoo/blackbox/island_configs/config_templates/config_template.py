from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List

import envs.monkey_zoo.blackbox.island_configs.config_templates
from infection_monkey.utils.plugins.plugin import Plugin


@dataclass
class ConfigValueDescriptor:
    path: str  # Dot separated config path. E.g. monkey.pba.actions.create_user
    content: Any  # Contents of config value. Depends on the type of config value.


class ConfigTemplate(Plugin, ABC):

    @staticmethod
    def base_package_name():
        return envs.monkey_zoo.blackbox.island_configs.config_templates.__package__

    @staticmethod
    def base_package_file():
        return envs.monkey_zoo.blackbox.island_configs.config_templates.__file__

    @abstractmethod
    @property
    def config_value_list(self) -> List[ConfigValueDescriptor]:
        pass

    @staticmethod
    def should_run(class_name: str) -> bool:
        return False
