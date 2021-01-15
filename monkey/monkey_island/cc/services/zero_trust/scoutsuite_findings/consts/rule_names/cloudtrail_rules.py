from enum import Enum


class CloudTrailRules(Enum):
    # Logging
    CLOUDTRAIL_DUPLICATED_GLOBAL_SERVICES_LOGGING = 'cloudtrail-duplicated-global-services-logging'
    CLOUDTRAIL_NO_DATA_LOGGING = 'cloudtrail-no-data-logging'
    CLOUDTRAIL_NO_GLOBAL_SERVICES_LOGGING = 'cloudtrail-no-global-services-logging'
    CLOUDTRAIL_NO_LOG_FILE_VALIDATION = 'cloudtrail-no-log-file-validation'
    CLOUDTRAIL_NO_LOGGING = 'cloudtrail-no-logging'
    CLOUDTRAIL_NOT_CONFIGURED = 'cloudtrail-not-configured'
