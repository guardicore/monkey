from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum


class CloudWatchRules(RuleNameEnum):
    # Logging
    CLOUDWATCH_ALARM_WITHOUT_ACTIONS = 'cloudwatch-alarm-without-actions'
