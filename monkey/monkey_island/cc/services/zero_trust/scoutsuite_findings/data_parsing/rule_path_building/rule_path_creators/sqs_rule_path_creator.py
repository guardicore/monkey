from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.sqs_rules import SQSRules
from ....consts.service_consts import SERVICE_TYPES


class SQSRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.SQS
    supported_rules = SQSRules
