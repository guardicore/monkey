from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.elbv2_rules import ELBv2Rules
from ....consts.service_consts import SERVICE_TYPES


class ELBv2RulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.ELB_V2
    supported_rules = ELBv2Rules
