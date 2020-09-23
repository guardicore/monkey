from enum import Enum


class RDSRules(Enum):
    # Encryption
    RDS_INSTANCE_STORAGE_NOT_ENCRYPTED = 'rds-instance-storage-not-encrypted'

    # Data loss prevention
    RDS_INSTANCE_BACKUP_DISABLED = 'rds-instance-backup-disabled'
    RDS_INSTANCE_SHORT_BACKUP_RETENTION_PERIOD = 'rds-instance-short-backup-retention-period'
    RDS_INSTANCE_SINGLE_AZ = 'rds-instance-single-az'
