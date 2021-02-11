from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum


class CloudTrailRules(RuleNameEnum):
    # Logging
    CLOUDTRAIL_DUPLICATED_GLOBAL_SERVICES_LOGGING = 'cloudtrail-duplicated-global-services-logging'
    CLOUDTRAIL_NO_DATA_LOGGING = 'cloudtrail-no-data-logging'
    CLOUDTRAIL_NO_GLOBAL_SERVICES_LOGGING = 'cloudtrail-no-global-services-logging'
    CLOUDTRAIL_NO_LOG_FILE_VALIDATION = 'cloudtrail-no-log-file-validation'
    CLOUDTRAIL_NO_LOGGING = 'cloudtrail-no-logging'
    CLOUDTRAIL_NOT_CONFIGURED = 'cloudtrail-not-configured'
