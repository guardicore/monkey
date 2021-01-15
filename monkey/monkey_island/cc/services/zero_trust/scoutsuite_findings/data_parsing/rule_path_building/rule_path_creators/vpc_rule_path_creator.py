from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.vpc_rules import VPCRules
from ....consts.service_consts import SERVICE_TYPES


class VPCRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.VPC
    supported_rules = VPCRules
