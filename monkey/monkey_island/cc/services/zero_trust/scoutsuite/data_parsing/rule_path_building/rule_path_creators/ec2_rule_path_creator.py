from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.ec2_rules import EC2Rules
from ....consts.service_consts import SERVICE_TYPES


class EC2RulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.EC2
    supported_rules = EC2Rules
