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

    # Permissive access rules
    S3_BUCKET_AUTHENTICATEDUSERS_WRITE_ACP = 's3-bucket-AuthenticatedUsers-write_acp'
    S3_BUCKET_AUTHENTICATEDUSERS_WRITE = 's3-bucket-AuthenticatedUsers-write'
    S3_BUCKET_AUTHENTICATEDUSERS_READ_ACP = 's3-bucket-AuthenticatedUsers-read_acp'
    S3_BUCKET_AUTHENTICATEDUSERS_READ = 's3-bucket-AuthenticatedUsers-read'
    S3_BUCKET_ALLUSERS_WRITE_ACP = 's3-bucket-AllUsers-write_acp'
    S3_BUCKET_ALLUSERS_WRITE = 's3-bucket-AllUsers-write'
    S3_BUCKET_ALLUSERS_READ_ACP = 's3-bucket-AllUsers-read_acp'
    S3_BUCKET_ALLUSERS_READ = 's3-bucket-AllUsers-read'
    S3_BUCKET_WORLD_PUT_POLICY = 's3-bucket-world-Put-policy'
    S3_BUCKET_WORLD_POLICY_STAR = 's3-bucket-world-policy-star'
    S3_BUCKET_WORLD_LIST_POLICY = 's3-bucket-world-List-policy'
    S3_BUCKET_WORLD_GET_POLICY = 's3-bucket-world-Get-policy'
    S3_BUCKET_WORLD_DELETE_POLICY = 's3-bucket-world-Delete-policy'
