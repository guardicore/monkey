from enum import Enum


class SESRules(Enum):

    # Permissive policies
    SES_IDENTITY_WORLD_SENDRAWEMAIL_POLICY = 'ses-identity-world-SendRawEmail-policy'
    SES_IDENTITY_WORLD_SENDEMAIL_POLICY = 'ses-identity-world-SendEmail-policy'
