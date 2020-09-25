from enum import Enum


class ELBv2Rules(Enum):
    # Encryption
    ELBV2_LISTENER_ALLOWING_CLEARTEXT = 'elbv2-listener-allowing-cleartext'
    ELBV2_OLDER_SSL_POLICY = 'elbv2-older-ssl-policy'

    # Logging
    ELBV2_NO_ACCESS_LOGS = 'elbv2-no-access-logs'

    # Data loss prevention
    ELBV2_NO_DELETION_PROTECTION = 'elbv2-no-deletion-protection'

    # Service security
    ELBV2_HTTP_REQUEST_SMUGGLING = 'elbv2-http-request-smuggling'
