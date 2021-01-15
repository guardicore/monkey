from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.cloudformation_rules import CloudformationRules
from ....consts.service_consts import SERVICE_TYPES


class CloudformationRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.CLOUDFORMATION
    supported_rules = CloudformationRules
