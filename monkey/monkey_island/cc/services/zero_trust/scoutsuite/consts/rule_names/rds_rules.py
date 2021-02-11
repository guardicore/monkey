from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum


class RDSRules(RuleNameEnum):
    # Encryption
    RDS_INSTANCE_STORAGE_NOT_ENCRYPTED = 'rds-instance-storage-not-encrypted'

    # Data loss prevention
    RDS_INSTANCE_BACKUP_DISABLED = 'rds-instance-backup-disabled'
    RDS_INSTANCE_SHORT_BACKUP_RETENTION_PERIOD = 'rds-instance-short-backup-retention-period'
    RDS_INSTANCE_SINGLE_AZ = 'rds-instance-single-az'

    # Firewalls
    RDS_SECURITY_GROUP_ALLOWS_ALL = 'rds-security-group-allows-all'
    RDS_SNAPSHOT_PUBLIC = 'rds-snapshot-public'

    # Service security
    RDS_INSTANCE_CA_CERTIFICATE_DEPRECATED = 'rds-instance-ca-certificate-deprecated'
    RDS_INSTANCE_NO_MINOR_UPGRADE = 'rds-instance-no-minor-upgrade'
