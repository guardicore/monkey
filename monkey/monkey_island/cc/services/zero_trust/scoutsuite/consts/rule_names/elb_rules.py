from enum import Enum


class ELBRules(Enum):
    # Logging
    ELB_NO_ACCESS_LOGS = 'elb-no-access-logs'

    # Encryption
    ELB_LISTENER_ALLOWING_CLEARTEXT = 'elb-listener-allowing-cleartext'
    ELB_OLDER_SSL_POLICY = 'elb-older-ssl-policy'
