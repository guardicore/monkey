from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.elb_rules import ELBRules
from ....consts.service_consts import SERVICE_TYPES


class ELBRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.ELB
    supported_rules = ELBRules
