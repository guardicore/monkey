from enum import Enum


class RedshiftRules(Enum):
    # Encryption
    REDSHIFT_CLUSTER_DATABASE_NOT_ENCRYPTED = 'redshift-cluster-database-not-encrypted'
    REDSHIFT_PARAMETER_GROUP_SSL_NOT_REQUIRED = 'redshift-parameter-group-ssl-not-required'

    # Firewalls
    REDSHIFT_SECURITY_GROUP_WHITELISTS_ALL = 'redshift-security-group-whitelists-all'

    # Restrictive Policies
    REDSHIFT_CLUSTER_PUBLICLY_ACCESSIBLE = 'redshift-cluster-publicly-accessible'

    # Logging
    REDSHIFT_PARAMETER_GROUP_LOGGING_DISABLED = 'redshift-parameter-group-logging-disabled'

    # Service security
    REDSHIFT_CLUSTER_NO_VERSION_UPGRADE = 'redshift-cluster-no-version-upgrade'
