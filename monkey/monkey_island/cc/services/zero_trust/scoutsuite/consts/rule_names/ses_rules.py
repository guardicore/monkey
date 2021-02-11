from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum


class SESRules(RuleNameEnum):

    # Permissive policies
    SES_IDENTITY_WORLD_SENDRAWEMAIL_POLICY = 'ses-identity-world-SendRawEmail-policy'
    SES_IDENTITY_WORLD_SENDEMAIL_POLICY = 'ses-identity-world-SendEmail-policy'
