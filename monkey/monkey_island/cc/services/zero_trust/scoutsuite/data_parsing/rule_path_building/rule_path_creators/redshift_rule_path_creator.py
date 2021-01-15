from ..abstract_rule_path_creator import AbstractRulePathCreator
from ....consts.rule_names.redshift_rules import RedshiftRules
from ....consts.service_consts import SERVICE_TYPES


class RedshiftRulePathCreator(AbstractRulePathCreator):

    service_type = SERVICE_TYPES.REDSHIFT
    supported_rules = RedshiftRules
