from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.ses_rules import SESRules
from ....consts.service_consts import SERVICE_TYPES


class SESRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.SES
    supported_rules = SESRules
