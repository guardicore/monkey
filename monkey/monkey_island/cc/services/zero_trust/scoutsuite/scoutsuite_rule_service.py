from monkey_island.cc.models.zero_trust.scoutsuite_rule import ScoutSuiteRule
from monkey_island.cc.services.zero_trust.scoutsuite.consts import rule_consts


class ScoutSuiteRuleService:

    @staticmethod
    def get_rule_from_rule_data(rule_data: dict) -> ScoutSuiteRule:
        rule = ScoutSuiteRule()
        rule.description = rule_data['description']
        rule.path = rule_data['path']
        rule.level = rule_data['level']
        rule.items = rule_data['items']
        rule.dashboard_name = rule_data['dashboard_name']
        rule.checked_items = rule_data['checked_items']
        rule.flagged_items = rule_data['flagged_items']
        rule.service = rule_data['service']
        rule.rationale = rule_data['rationale']
        rule.remediation = rule_data['remediation']
        rule.compliance = rule_data['compliance']
        rule.references = rule_data['references']
        return rule

    @staticmethod
    def is_rule_dangerous(rule: ScoutSuiteRule):
        return rule.level == rule_consts.RULE_LEVEL_DANGER and len(rule.items) != 0

    @staticmethod
    def is_rule_warning(rule: ScoutSuiteRule):
        return rule.level == rule_consts.RULE_LEVEL_WARNING and len(rule.items) != 0
