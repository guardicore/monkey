from enum import Enum


class IAMRules(Enum):
    # Authentication/authorization
    IAM_USER_NO_ACTIVE_KEY_ROTATION = 'iam-user-no-Active-key-rotation'
    IAM_PASSWORD_POLICY_MINIMUM_LENGTH = 'iam-password-policy-minimum-length'
    IAM_PASSWORD_POLICY_NO_EXPIRATION = 'iam-password-policy-no-expiration'
    IAM_PASSWORD_POLICY_REUSE_ENABLED = 'iam-password-policy-reuse-enabled'
    IAM_USER_WITH_PASSWORD_AND_KEY = 'iam-user-with-password-and-key'
    IAM_ASSUME_ROLE_LACKS_EXTERNAL_ID_AND_MFA = 'iam-assume-role-lacks-external-id-and-mfa'
    IAM_USER_WITHOUT_MFA = 'iam-user-without-mfa'
    IAM_ROOT_ACCOUNT_NO_MFA = 'iam-root-account-no-mfa'
    IAM_ROOT_ACCOUNT_WITH_ACTIVE_KEYS = 'iam-root-account-with-active-keys'
    IAM_USER_NO_INACTIVE_KEY_ROTATION = 'iam-user-no-Inactive-key-rotation'
    IAM_USER_WITH_MULTIPLE_ACCESS_KEYS = 'iam-user-with-multiple-access-keys'

    # Least privilege
    IAM_ASSUME_ROLE_POLICY_ALLOWS_ALL = 'iam-assume-role-policy-allows-all'
    IAM_EC2_ROLE_WITHOUT_INSTANCES = 'iam-ec2-role-without-instances'
    IAM_GROUP_WITH_INLINE_POLICIES = 'iam-group-with-inline-policies'
    IAM_GROUP_WITH_NO_USERS = 'iam-group-with-no-users'
    IAM_INLINE_GROUP_POLICY_ALLOWS_IAM_PASSROLE = 'iam-inline-group-policy-allows-iam-PassRole'
    IAM_INLINE_GROUP_POLICY_ALLOWS_NOTACTIONS = 'iam-inline-group-policy-allows-NotActions'
    IAM_INLINE_GROUP_POLICY_ALLOWS_STS_ASSUMEROLE = 'iam-inline-group-policy-allows-sts-AssumeRole'
    IAM_INLINE_ROLE_POLICY_ALLOWS_IAM_PASSROLE = 'iam-inline-role-policy-allows-iam-PassRole'
    IAM_INLINE_ROLE_POLICY_ALLOWS_NOTACTIONS = 'iam-inline-role-policy-allows-NotActions'
    IAM_INLINE_ROLE_POLICY_ALLOWS_STS_ASSUMEROLE = 'iam-inline-role-policy-allows-sts-AssumeRole'
    IAM_INLINE_USER_POLICY_ALLOWS_IAM_PASSROLE = 'iam-inline-user-policy-allows-iam-PassRole'
    IAM_INLINE_USER_POLICY_ALLOWS_NOTACTIONS = 'iam-inline-user-policy-allows-NotActions'
    IAM_INLINE_USER_POLICY_ALLOWS_STS_ASSUMEROLE = 'iam-inline-user-policy-allows-sts-AssumeRole'
    IAM_MANAGED_POLICY_ALLOWS_IAM_PASSROLE = 'iam-managed-policy-allows-iam-PassRole'
    IAM_MANAGED_POLICY_ALLOWS_NOTACTIONS = 'iam-managed-policy-allows-NotActions'
    IAM_MANAGED_POLICY_ALLOWS_STS_ASSUMEROLE = 'iam-managed-policy-allows-sts-AssumeRole'
    IAM_MANAGED_POLICY_NO_ATTACHMENTS = 'iam-managed-policy-no-attachments'
    IAM_ROLE_WITH_INLINE_POLICIES = 'iam-role-with-inline-policies'
    IAM_ROOT_ACCOUNT_USED_RECENTLY = 'iam-root-account-used-recently'
    IAM_ROOT_ACCOUNT_WITH_ACTIVE_CERTS = 'iam-root-account-with-active-certs'
    IAM_USER_WITH_INLINE_POLICIES = 'iam-user-with-inline-policies'
