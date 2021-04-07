from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.elbv2_rules import ELBv2Rules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.service_consts import SERVICE_TYPES
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.abstract_rule_path_creator import (  # noqa: E501
    AbstractRulePathCreator,
)


class ELBv2RulePathCreator(AbstractRulePathCreator):
    service_type = SERVICE_TYPES.ELB_V2
    supported_rules = ELBv2Rules
