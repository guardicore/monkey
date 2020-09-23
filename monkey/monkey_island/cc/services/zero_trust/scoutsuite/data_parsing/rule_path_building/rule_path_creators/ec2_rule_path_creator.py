from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.ec2_rules import EC2Rules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.service_consts import \
    SERVICE_TYPES
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.abstract_rule_path_creator import \
    AbstractRulePathCreator


class EC2RulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.EC2
    supported_rules = EC2Rules
