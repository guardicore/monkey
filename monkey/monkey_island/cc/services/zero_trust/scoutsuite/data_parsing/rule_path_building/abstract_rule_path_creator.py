from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Type

from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum
from monkey_island.cc.services.zero_trust.scoutsuite.consts.service_consts import FINDINGS, SERVICES, SERVICE_TYPES


class AbstractRulePathCreator(ABC):

    @property
    @abstractmethod
    def service_type(self) -> SERVICE_TYPES:
        pass

    @property
    @abstractmethod
    def supported_rules(self) -> Type[RuleNameEnum]:
        pass

    @classmethod
    def build_rule_path(cls, rule_name: Enum) -> List[str]:
        assert(rule_name in cls.supported_rules)
        return [SERVICES, cls.service_type.value, FINDINGS, rule_name.value]
