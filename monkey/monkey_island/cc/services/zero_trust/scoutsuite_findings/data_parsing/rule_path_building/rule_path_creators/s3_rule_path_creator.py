from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.s3_rules import S3Rules
from ....consts.service_consts import SERVICE_TYPES


class S3RulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.S3
    supported_rules = S3Rules
