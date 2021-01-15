from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.iam_rules import IAMRules
from ....consts.service_consts import SERVICE_TYPES


class IAMRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.IAM
    supported_rules = IAMRules
