from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.vpc_rules import VPCRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.service_consts import SERVICE_TYPES
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.abstract_rule_path_creator import \
    AbstractRulePathCreator


class VPCRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.VPC
    supported_rules = VPCRules
