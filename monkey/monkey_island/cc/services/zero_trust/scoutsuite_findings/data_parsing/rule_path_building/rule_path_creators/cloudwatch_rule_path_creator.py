from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.cloudwatch_rules import CloudWatchRules
from ....consts.service_consts import SERVICE_TYPES


class CloudWatchRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.CLOUDWATCH
    supported_rules = CloudWatchRules
