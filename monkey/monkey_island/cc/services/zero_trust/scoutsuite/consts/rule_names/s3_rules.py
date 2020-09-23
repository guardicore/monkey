from enum import Enum


class S3Rules(Enum):
    # Encryption
    S3_BUCKET_ALLOWING_CLEARTEXT = 's3-bucket-allowing-cleartext'
    S3_BUCKET_NO_DEFAULT_ENCRYPTION = 's3-bucket-no-default-encryption'

    # Data loss prevention
    S3_BUCKET_NO_MFA_DELETE = 's3-bucket-no-mfa-delete'
    S3_BUCKET_NO_VERSIONING = 's3-bucket-no-versioning'

    # Logging
    S3_BUCKET_NO_LOGGING = 's3-bucket-no-logging'
