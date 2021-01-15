from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.cloudtrail_rules import CloudTrailRules
from ....consts.service_consts import SERVICE_TYPES


class CloudTrailRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.CLOUDTRAIL
    supported_rules = CloudTrailRules
