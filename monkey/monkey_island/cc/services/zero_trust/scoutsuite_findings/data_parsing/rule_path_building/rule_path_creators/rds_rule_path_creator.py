from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.rds_rules import RDSRules
from ....consts.service_consts import SERVICE_TYPES


class RDSRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.RDS
    supported_rules = RDSRules
