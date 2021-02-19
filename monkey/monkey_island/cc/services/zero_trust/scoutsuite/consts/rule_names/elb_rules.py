from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum


class ELBRules(RuleNameEnum):
    # Logging
    ELB_NO_ACCESS_LOGS = 'elb-no-access-logs'

    # Encryption
    ELB_LISTENER_ALLOWING_CLEARTEXT = 'elb-listener-allowing-cleartext'
    ELB_OLDER_SSL_POLICY = 'elb-older-ssl-policy'
