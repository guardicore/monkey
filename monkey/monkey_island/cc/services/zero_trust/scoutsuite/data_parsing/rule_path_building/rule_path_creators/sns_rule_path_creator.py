from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.sns_rules import SNSRules
from ....consts.service_consts import SERVICE_TYPES


class SNSRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.SNS
    supported_rules = SNSRules
