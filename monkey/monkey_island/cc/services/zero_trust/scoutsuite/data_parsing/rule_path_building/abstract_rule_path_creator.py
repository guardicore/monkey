from abc import ABC, abstractmethod
from typing import List, Union

from monkey_island.cc.services.zero_trust.scoutsuite.consts.ec2_rules import EC2Rules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.service_consts import SERVICES, FINDINGS, SERVICE_TYPES


class AbstractRulePathCreator(ABC):

    @property
    @abstractmethod
    def service_type(self) -> SERVICE_TYPES:
        pass

    @property
    @abstractmethod
    def supported_rules(self) -> List[Union[EC2Rules]]:
        pass

    @classmethod
    def build_rule_path(cls, rule_name: Union[EC2Rules]) -> List[str]:
        assert(rule_name in cls.supported_rules)
        return [SERVICES, cls.service_type.value, FINDINGS, rule_name.value]
